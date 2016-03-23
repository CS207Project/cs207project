from .ast import *

class PrettyPrint(ASTVisitor):
    def __init__(self):
        pass
    def visit(self, node):
        print(node.__class__.__name__)
        for child in node.children:
            self.visit(child)

class CheckSingleAssignment(ASTVisitor):
    def __init__(self):
        self.globalAssignments = set()
        self.localAssignments = set()
    def visit(self, node):
        if isinstance(node, ASTProgram):
            for child in node.children:
                self.visit( child )
        elif isinstance(node, ASTComponent):
            self.localAssignments = set() # wipe the local set for each component
            self.globalAssignments.add(node.name.name)
            for child in node.children:
                if isinstance(child, ASTAssignmentExpr):
                    if ((child.binding.name in self.globalAssignments) or
                        (child.binding.name in self.localAssignments)):
                        raise SyntaxError("Double Assignment of {} not allowed".format(child.binding.name))
                    else:
                        self.localAssignments.add(child.binding.name)
