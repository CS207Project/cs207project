from .ast import *
from .symtab import *
from .lib_import import LibraryImporter

class SymbolTableVisitor(ASTVisitor):
  def __init__(self):
    self.symbol_table = SymbolTable()

  def return_value(self):
    return self.symbol_table

  def visit(self, node):
    if isinstance(node, ASTImport):
      # Import statements make library functions available to PyPE
      imp = LibraryImporter(node.module)
      imp.add_symbols(self.symbol_table)

    # Add symbols for the following types of names:
    elif isinstance(node, ASTInputExpr):
    #   inputs/outputs: anything in an input or output expression
    #     the SymbolType should be input or output, and the ref can be None
    #     the scope should be the enclosing component
        for child in node.children:
            self.symbol_table.addsym(Symbol(child.name, SymbolType.input, None),
                scope = node.parent.name.name)

    elif isinstance(node, ASTAssignmentExpr):
    #   assigned names: the bound name in an assignment expression
    #     the SymbolType should be var, and the ref can be None
    #     the scope should be the enclosing component
        self.symbol_table.addsym(Symbol(node.binding.name, SymbolType.var, None),
            scope = node.parent.name.name)

    elif isinstance(node, ASTComponent):
    #   components: the name of each component
    #     the SymbolType should be component, and the ref can be None
    #     the scope sould be *global*
        self.symbol_table.addsym(Symbol(node.name.name, SymbolType.component, None))

        # recursively call 'visit' on all children
        for child in node.children:
            self.visit(child)

    elif isinstance(node, ASTProgram):
        # recursively call 'visit' on all children
        for child in node.children:
            self.visit(child)

    # Note, you'll need to track scopes again for some of these.
    # You may need to add class state to handle this.
