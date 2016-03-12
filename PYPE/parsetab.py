
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'D3A842A66F1699B57867968AA7CCDDEA'
    
_lr_action_items = {'OP_ADD':([13,],[21,]),'LPAREN':([0,1,5,6,8,9,10,12,14,15,16,17,18,19,20,21,22,24,25,26,27,28,30,31,32,33,34,35,36,37,38,39,40,41,42,43,46,47,48,49,50,51,53,54,55,57,58,],[2,-4,-5,2,13,-3,-2,-27,-9,13,-26,-28,-6,29,13,13,13,13,13,29,-8,-7,29,-13,-17,-15,13,-30,13,13,-21,13,13,13,29,-11,-12,-14,-29,-23,-22,-20,-24,-25,-10,-19,-16,]),'STRING':([8,12,14,15,16,17,20,21,22,24,25,27,31,34,35,36,37,38,39,40,41,43,46,48,49,50,51,53,54,55,57,],[17,-27,-9,17,-26,-28,17,17,17,17,17,-8,-13,17,-30,17,17,-21,17,17,17,-11,-12,-29,-23,-22,-20,-24,-25,-10,-19,]),'OP_SUB':([13,],[20,]),'RPAREN':([11,12,16,17,19,22,26,30,31,32,33,34,35,36,37,38,40,41,42,43,46,47,48,49,50,51,52,53,54,55,56,57,58,],[18,-27,-26,-28,31,38,43,46,-13,-17,-15,49,-30,50,51,-21,53,54,55,-11,-12,-14,-29,-23,-22,-20,57,-24,-25,-10,58,-19,-16,]),'ID':([4,7,8,12,13,14,15,16,17,19,20,21,22,23,24,25,26,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,53,54,55,57,58,],[8,11,16,-27,22,-9,16,-26,-28,32,16,16,16,39,16,16,32,-8,45,32,-13,-17,-15,16,-30,16,16,-21,16,16,16,32,-11,56,-18,-12,-14,-29,-23,-22,-20,-24,-25,-10,-19,-16,]),'RBRACE':([12,14,15,16,17,27,31,38,43,46,49,50,51,53,54,55,57,],[-27,-9,28,-26,-28,-8,-13,-21,-11,-12,-23,-22,-20,-24,-25,-10,-19,]),'IMPORT':([2,],[7,]),'NUMBER':([8,12,14,15,16,17,20,21,22,24,25,27,31,34,35,36,37,38,39,40,41,43,46,48,49,50,51,53,54,55,57,],[12,-27,-9,12,-26,-28,12,12,12,12,12,-8,-13,12,-30,12,12,-21,12,12,12,-11,-12,-29,-23,-22,-20,-24,-25,-10,-19,]),'LBRACE':([0,1,5,6,9,10,18,28,],[4,-4,-5,4,-3,-2,-6,-7,]),'$end':([1,3,5,6,9,10,18,28,],[-4,0,-5,-1,-3,-2,-6,-7,]),'ASSIGN':([13,],[23,]),'OP_MUL':([13,],[24,]),'OUTPUT':([13,],[19,]),'OP_DIV':([13,],[25,]),'INPUT':([13,],[26,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'import_statement':([0,6,],[1,9,]),'expression_list':([8,],[15,]),'program':([0,],[3,]),'declaration':([19,26,30,42,],[33,33,47,47,]),'type':([29,],[44,]),'expression':([8,15,20,21,22,24,25,34,36,37,39,40,41,],[14,27,35,35,35,35,35,48,48,48,52,48,48,]),'component':([0,6,],[5,10,]),'parameter_list':([20,21,22,24,25,],[34,36,37,40,41,]),'declaration_list':([19,26,],[30,42,]),'statement_list':([0,],[6,]),}

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