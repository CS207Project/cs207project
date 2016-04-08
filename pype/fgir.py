import enum

FGNodeType = enum.Enum('FGNodeType','component libraryfunction librarymethod input output assignment literal forward unknown')


class FGNode(object):
  def __init__(self, nodeid, nodetype, ref=None, inputs=[]):
    self.nodeid = nodeid
    self.type = nodetype
    self.ref = ref
    self.inputs = inputs
    if nodetype is FGNodeType.libraryfunction:
      print(type(ref))

  def __repr__(self):
    return '<'+str(self.type)+' '+str(self.nodeid)+'<='+','.join(map(str,self.inputs))+' : '+str(self.ref)+'>'

class Flowgraph(object):
  def __init__(self, name='?'):
    self.name = name
    self.variables = {} # { str -> nodeid }
    self.nodes = {} # { nodeid -> Node }
    self.inputs = [] # [ nodeid, ... ]
    self.outputs = [] # [ nodeid, ... ]
    self._id_counter = 0

  def new_node(self,nodetype,ref=None):
    nid = '@N'+str(self._id_counter)
    self._id_counter += 1
    node = FGNode(nid, nodetype, ref, [])
    self.nodes[nid] = node
    return node

  def get_var(self, name):
    return self.variables.get(name, None)

  def set_var(self, name, nodeid):
    self.variables[name] = nodeid

  def add_input(self, nodeid):
    self.inputs.append(nodeid)

  def add_output(self, nodeid):
    self.outputs.append(nodeid)

  def dotfile(self):
    s = ''
    s+= 'digraph '+self.name+' {\n'
    for (src,node) in self.nodes.items():
      for dst in node.inputs:
        s+= '  "'+str(dst)+'" -> "'+str(src)+'"\n'
    for (var,nid) in self.variables.items():
      s+= '  "'+str(nid)+'" [ label = "'+str(var)+'" ]\n'
    for nid in self.inputs:
      s+= '  "'+str(nid)+'" [ color = "green" ]\n'
    for nid in self.outputs:
      s+= '  "'+str(nid)+'" [ color = "red" ]\n'
    s+= '}\n'
    return s


  def pre(self, nodeid):
    return self.nodes[nodeid].inputs

  def post(self, nodeid):
    return [i for (i,n) in self.nodes.items() if nodeid in self.nodes[i].inputs]

  def topological_sort(self):
    topo_sorted = []
    nodes_left = list(self.nodes.keys())

    while len(nodes_left) > 0:
      nid = nodes_left[0]
      self.topo_vistnode(nid,nodes_left,topo_sorted)

    return topo_sorted # should return a list of node ids in sorted order

  def topo_vistnode(self,nid,nodes_left,topo_sorted):
    if nid in topo_sorted:
      return
    for i_nid in self.nodes[nid].inputs:
      self.topo_vistnode(i_nid,nodes_left,topo_sorted)

    nodes_left.remove(nid)
    topo_sorted.append(nid)
    return

class FGIR(object):
  def __init__(self):
    self.graphs = {} # { component_name:str => Flowgraph }

  def __getitem__(self, component):
    return self.graphs[component]

  def __setitem__(self, component, flowgraph):
    self.graphs[component] = flowgraph

  def __iter__(self):
    for component in self.graphs:
      yield component

  def flowgraph_pass(self, flowgraph_optimizer):
    for component in self.graphs:
      fg = flowgraph_optimizer.visit(self.graphs[component])
      if fg is not None:
        self.graphs[component] = fg

  def node_pass(self, node_optimizer, *args, topological=False):
    for component in self.graphs:
      fg = self.graphs[component]
      if topological:
        node_order = fg.topological_sort()
      else:
        node_order = fg.nodes.keys()
      for node in node_order:
        n = node_optimizer.visit(fg.nodes[node])
        if n is not None:
          fg.nodes[node] = n

  def topological_node_pass(self, topo_optimizer):
    self.node_pass(topo_optimizer, topological=True)

  def _topo_helper(self, name, deps, order=[]):
    for dep in deps[name]:
      if dep not in order:
        order = self._topo_helper(dep, deps, order)
    return order+[name]

  def topological_flowgraph_pass(self, topo_flowgraph_optimizer):
    deps = {}
    for (name,fg) in self.graphs.items():
      deps[name] = [n.ref for n in fg.nodes.values() if n.type==FGNodeType.component]
    order = []
    for name in self.graphs:
      order = self._topo_helper(name, deps, order)
    for name in order:
      fg = topo_flowgraph_optimizer.visit(self.graphs[name])
      if fg is not None:
        self.graphs[name] = fg
