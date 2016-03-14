
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = '2D1291BA64AFE1598D29C55C8A54EBFE'
    
_lr_action_items = {'OP_SUB':([12,],[18,]),'LPAREN':([0,4,5,6,7,9,10,11,13,14,15,16,18,19,20,21,22,24,25,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,48,49,50,51,52,54,55,57,58,],[3,3,-4,-5,12,-3,-2,-9,-26,-28,12,-27,12,31,12,12,12,12,31,-8,-7,-6,-30,12,31,-15,-13,-17,12,-21,12,12,12,12,31,-11,-29,-23,-14,-12,-24,-20,-25,-22,-10,-19,-16,]),'OUTPUT':([12,],[19,]),'IMPORT':([3,],[8,]),'OP_MUL':([12,],[20,]),'ID':([1,7,8,11,12,13,14,15,16,18,19,20,21,22,23,24,25,26,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,55,57,58,],[7,13,17,-9,21,-26,-28,13,-27,13,35,13,13,13,40,13,35,-8,-30,13,46,35,-15,-13,-17,13,-21,13,13,13,13,35,-11,-29,-23,-18,56,-14,-12,-24,-20,-25,-22,-10,-19,-16,]),'$end':([2,4,5,6,9,10,27,28,],[0,-1,-4,-5,-3,-2,-7,-6,]),'OP_DIV':([12,],[22,]),'NUMBER':([7,11,13,14,15,16,18,20,21,22,24,26,29,30,34,36,37,38,39,40,41,43,44,45,49,50,51,52,54,55,57,],[16,-9,-26,-28,16,-27,16,16,16,16,16,-8,-30,16,-13,16,-21,16,16,16,16,-11,-29,-23,-12,-24,-20,-25,-22,-10,-19,]),'OP_ADD':([12,],[24,]),'STRING':([7,11,13,14,15,16,18,20,21,22,24,26,29,30,34,36,37,38,39,40,41,43,44,45,49,50,51,52,54,55,57,],[14,-9,-26,-28,14,-27,14,14,14,14,14,-8,-30,14,-13,14,-21,14,14,14,14,-11,-29,-23,-12,-24,-20,-25,-22,-10,-19,]),'ASSIGN':([12,],[23,]),'LBRACE':([0,4,5,6,9,10,27,28,],[1,1,-4,-5,-3,-2,-7,-6,]),'RBRACE':([11,13,14,15,16,26,34,37,43,45,49,50,51,52,54,55,57,],[-9,-26,-28,27,-27,-8,-13,-21,-11,-23,-12,-24,-20,-25,-22,-10,-19,]),'INPUT':([12,],[25,]),'RPAREN':([13,14,16,17,19,21,25,29,30,32,33,34,35,36,37,38,39,41,42,43,44,45,48,49,50,51,52,53,54,55,56,57,58,],[-26,-28,-27,28,34,37,43,-30,45,49,-15,-13,-17,50,-21,51,52,54,55,-11,-29,-23,-14,-12,-24,-20,-25,57,-22,-10,58,-19,-16,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'declaration':([19,25,32,42,],[33,33,48,48,]),'program':([0,],[2,]),'statement_list':([0,],[4,]),'parameter_list':([18,20,21,22,24,],[30,36,38,39,41,]),'declaration_list':([19,25,],[32,42,]),'expression_list':([7,],[15,]),'import_statement':([0,4,],[5,9,]),'component':([0,4,],[6,10,]),'expression':([7,15,18,20,21,22,24,30,36,38,39,40,41,],[11,26,29,29,29,29,29,44,44,44,44,53,44,]),'type':([31,],[47,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement_list','program',1,'p_program','parser.py',8),
  ('statement_list -> statement_list component','statement_list',2,'p_statement_list','parser.py',13),
  ('statement_list -> statement_list import_statement','statement_list',2,'p_statement_list','parser.py',14),
  ('statement_list -> import_statement','statement_list',1,'p_statement_list','parser.py',15),
  ('statement_list -> component','statement_list',1,'p_statement_list','parser.py',16),
  ('import_statement -> LPAREN IMPORT ID RPAREN','import_statement',4,'p_import_statement','parser.py',23),
  ('component -> LBRACE ID expression_list RBRACE','component',4,'p_component','parser.py',27),
  ('expression_list -> expression_list expression','expression_list',2,'p_expression_list','parser.py',31),
  ('expression_list -> expression','expression_list',1,'p_expression_list','parser.py',32),
  ('expression -> LPAREN INPUT declaration_list RPAREN','expression',4,'p_input','parser.py',39),
  ('expression -> LPAREN INPUT RPAREN','expression',3,'p_input','parser.py',40),
  ('expression -> LPAREN OUTPUT declaration_list RPAREN','expression',4,'p_output','parser.py',48),
  ('expression -> LPAREN OUTPUT RPAREN','expression',3,'p_output','parser.py',49),
  ('declaration_list -> declaration_list declaration','declaration_list',2,'p_declaration_list','parser.py',57),
  ('declaration_list -> declaration','declaration_list',1,'p_declaration_list','parser.py',58),
  ('declaration -> LPAREN type ID RPAREN','declaration',4,'p_declaration','parser.py',66),
  ('declaration -> ID','declaration',1,'p_declaration','parser.py',67),
  ('type -> ID','type',1,'p_type','parser.py',75),
  ('expression -> LPAREN ASSIGN ID expression RPAREN','expression',5,'p_assign','parser.py',80),
  ('expression -> LPAREN ID parameter_list RPAREN','expression',4,'p_functioncall','parser.py',85),
  ('expression -> LPAREN ID RPAREN','expression',3,'p_functioncall','parser.py',86),
  ('expression -> LPAREN OP_ADD parameter_list RPAREN','expression',4,'p_operator','parser.py',95),
  ('expression -> LPAREN OP_SUB parameter_list RPAREN','expression',4,'p_operator','parser.py',96),
  ('expression -> LPAREN OP_MUL parameter_list RPAREN','expression',4,'p_operator','parser.py',97),
  ('expression -> LPAREN OP_DIV parameter_list RPAREN','expression',4,'p_operator','parser.py',98),
  ('expression -> ID','expression',1,'p_identification','parser.py',108),
  ('expression -> NUMBER','expression',1,'p_literal','parser.py',112),
  ('expression -> STRING','expression',1,'p_literal','parser.py',113),
  ('parameter_list -> parameter_list expression','parameter_list',2,'p_parameter_list','parser.py',121),
  ('parameter_list -> expression','parameter_list',1,'p_parameter_list','parser.py',122),
]
