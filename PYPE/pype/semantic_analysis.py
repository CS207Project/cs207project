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
        self.assignments = set()
    def visit(self, node):
        if isinstance(node, ASTProgram):
            for child in node.children:
                self.assignments = set() # wipe the set for each component
                self.visit( child )
        elif isinstance(node, ASTComponent):
            for child in node.children:
                if isinstance(child, ASTAssignmentExpr):
                    if child.binding in self.assignments:
                            raise StandardError("Double Assignment of {} not allowed".format(child.binding)
                    else:
                        self.assignments.add(child.binding)
