from .fgir import *
from .error import *

# Optimization pass interfaces

class Optimization(object):
  def visit(self, obj): pass

class FlowgraphOptimization(Optimization):
  '''Called on each flowgraph in a FGIR.

  May modify the flowgraph by adding or removing nodes (return a new Flowgraph).
  If you modify nodes, make sure inputs, outputs, and variables are all updated.
  May NOT add or remove flowgraphs.'''
  pass

class TopologicalFlowgraphOptimization(Optimization):
  '''Called on each flowgraph in a FGIR, in dependent order.

  Components which are used by other components will be called first.'''
  pass

class NodeOptimization(Optimization):
  '''Called on each node in a FGIR.

  May modify the node (return a new Node object, and it will be assigned).
  May NOT remove or add nodes (use a component pass).'''
  pass

class TopologicalNodeOptimization(NodeOptimization): pass

# Optimization pass implementations

class PrintIR(TopologicalNodeOptimization):
  'A simple "optimization" pass which can be used to debug topological sorting'
  def visit(self, node):
    print(str(node))

class AssignmentEllision(FlowgraphOptimization):
  '''Eliminates all assignment nodes.

  Assignment nodes are useful for the programmer to reuse the output of an
  expression multiple times, and the lowering transformation generates explicit
  flowgraph nodes for these expressions. However, they are not necessary for
  execution, as they simply forward their value. This removes them and connects
  their pre- and post-dependencies.'''

  def visit(self, flowgraph):
    nid_varname = dict((v,k) for k,v in flowgraph.variables.items()) # make a reverse dictionary so that you can remove things
    nodes_to_del = []

    for (nid,node) in flowgraph.nodes.items(): # loop over the nodes
      if node.type == FGNodeType.assignment: # find the assignments
        inp = node.inputs.pop() # get it's parent
        nodes_to_del.append(nid)

        # update variable name
        if nid in nid_varname.keys():
          flowgraph.variables[nid_varname[nid]] = inp

        # update edges
        for (j_nid,j_node) in flowgraph.nodes.items():
          if nid in j_node.inputs:
            j_node.inputs = list(filter(lambda a: a != nid,j_node.inputs))
            j_node.inputs.append(inp)

    # delete the nodes
    for nid in nodes_to_del:
      del flowgraph.nodes[nid]

    return flowgraph


class DeadCodeElimination(FlowgraphOptimization):
  '''Eliminates unreachable expression statements.

  Statements which never affect any output are effectively useless, and we call
  these "dead code" blocks. This optimization removes any expressions which can
  be shown not to affect the output.
  NOTE: input statements *cannot* safely be removed, since doing so would change
  the call signature of the component. For example, it might seem that the input
  x could be removed:
    { component1 (input x y) (output y) }
  but imagine this component1 was in a file alongside this one:
    { component2 (input a b) (:= c (component a b)) (output c) }
  By removing x from component1, it could no longer accept two arguments. So in
  this instance, component1 will end up unmodified after DCE.'''

  def visit(self, flowgraph):
    nid_varname = dict((v,k) for k,v in flowgraph.variables.items()) # reverse dicitonary

    nodes_to_del = list(flowgraph.nodes.keys())
    outs = flowgraph.outputs[:]

    # start with the outputs and resursively remove from consideration things
    # that the output needs
    while(len(outs) > 0):
      nid = outs.pop()
      if nid in nodes_to_del:
        nodes_to_del.remove(nid)

      for j_nid in flowgraph.nodes[nid].inputs:
        outs.append(j_nid)


    # now we have the nodes we need to remove
    # they need to be removed from the nodes list, input lists and variables
    for nid in nodes_to_del:
      if nid in flowgraph.inputs:
        continue

      # update variable name
      if nid in nid_varname.keys():
        del flowgraph.variables[nid_varname[nid]]

      # remove the node entirely
      del flowgraph.nodes[nid]
    return flowgraph

class InlineComponents(TopologicalFlowgraphOptimization):
  '''Replaces every component invocation with a copy of that component's flowgraph.

  Topological order guarantees that we inline components before they are invoked.'''
  def __init__(self):
    self.component_cache = {}

  def visit(self, flowgraph):
    for (cnode_id, cnode) in [(nid,n) for (nid,n) in flowgraph.nodes.items() if n.type==FGNodeType.component]:
      target = self.component_cache[cnode.ref]
      # Add a copy of every node in target flowgraph
      id_map = {} # maps node id's in the target to node id's in our flowgraph
      for tnode in target.nodes.values():
        if tnode.type==FGNodeType.input or tnode.type==FGNodeType.output:
          newtype = FGNodeType.forward
        else:
          newtype = tnode.type
        n = flowgraph.new_node(newtype, ref=tnode.ref)
        id_map[tnode.nodeid] = n.nodeid
      # Connect all copies together
      for tid,tnode in target.nodes.items():
        flowgraph.nodes[id_map[tid]].inputs = [id_map[i] for i in tnode.inputs]
      # Link inputs of cnode to inputs of target flowgraph
      for cnode_input,targ_input in zip(cnode.inputs, target.inputs):
        flowgraph.nodes[id_map[targ_input]].inputs = [cnode_input]
      # Link output of target flowgraph to outputs of cnode
      for oid,onode in flowgraph.nodes.items():
        if cnode_id in onode.inputs:
          onode.inputs[onode.inputs.index(cnode_id)] = id_map[target.outputs[0]]
      # Remove all other references to cnode in flowgraph
      del flowgraph.nodes[cnode_id]
      victims = [s for s,nid in flowgraph.variables.items() if nid==cnode_id]
      for v in victims:
        del flowgraph.variables[v]
    self.component_cache[flowgraph.name] = flowgraph
    return flowgraph
