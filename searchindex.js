Search.setIndex({envversion:47,filenames:["api/go_server","api/go_server_persistent","api/go_webserver","api/modules","api/procs","api/pype","api/timeseries","api/tsdb","api/vptrees","api/webserver","api/webutils","authors","changes","index","license"],objects:{"":{go_server:[0,0,0,"-"],go_server_persistent:[1,0,0,"-"],go_webserver:[2,0,0,"-"],procs:[4,0,0,"-"],pype:[5,0,0,"-"],timeseries:[6,0,0,"-"],tsdb:[7,0,0,"-"],vptrees:[8,0,0,"-"],webserver:[9,0,0,"-"],webutils:[10,0,0,"-"]},"procs.corr":{main:[4,4,1,""],proc_main:[4,4,1,""]},"procs.junk":{main:[4,4,1,""]},"procs.stats":{main:[4,4,1,""],proc_main:[4,4,1,""]},"pype.ast":{ASTAssignmentExpr:[5,2,1,""],ASTComponent:[5,2,1,""],ASTEvalExpr:[5,2,1,""],ASTID:[5,2,1,""],ASTImport:[5,2,1,""],ASTInputExpr:[5,2,1,""],ASTLiteral:[5,2,1,""],ASTModVisitor:[5,2,1,""],ASTNode:[5,2,1,""],ASTOutputExpr:[5,2,1,""],ASTProgram:[5,2,1,""],ASTVisitor:[5,2,1,""]},"pype.ast.ASTAssignmentExpr":{binding:[5,3,1,""],value:[5,3,1,""]},"pype.ast.ASTComponent":{expressions:[5,3,1,""],name:[5,3,1,""]},"pype.ast.ASTEvalExpr":{args:[5,3,1,""],op:[5,3,1,""]},"pype.ast.ASTModVisitor":{post_visit:[5,1,1,""],visit:[5,1,1,""]},"pype.ast.ASTNode":{children:[5,3,1,""],mod_walk:[5,1,1,""],pprint:[5,1,1,""],walk:[5,1,1,""]},"pype.ast.ASTVisitor":{return_value:[5,1,1,""],visit:[5,1,1,""]},"pype.error":{PypeSyntaxError:[5,8,1,""],PypeTypeError:[5,8,1,""],Warn:[5,4,1,""]},"pype.fgir":{FGIR:[5,2,1,""],FGNode:[5,2,1,""],FGNodeType:[5,2,1,""],Flowgraph:[5,2,1,""]},"pype.fgir.FGIR":{flowgraph_pass:[5,1,1,""],node_pass:[5,1,1,""],topological_flowgraph_pass:[5,1,1,""],topological_node_pass:[5,1,1,""]},"pype.fgir.FGNodeType":{assignment:[5,3,1,""],component:[5,3,1,""],forward:[5,3,1,""],input:[5,3,1,""],libraryfunction:[5,3,1,""],librarymethod:[5,3,1,""],literal:[5,3,1,""],output:[5,3,1,""],unknown:[5,3,1,""]},"pype.fgir.Flowgraph":{add_input:[5,1,1,""],add_output:[5,1,1,""],dotfile:[5,1,1,""],get_var:[5,1,1,""],new_node:[5,1,1,""],post:[5,1,1,""],pre:[5,1,1,""],set_var:[5,1,1,""],topo_vistnode:[5,1,1,""],topological_sort:[5,1,1,""]},"pype.lexer":{find_column:[5,4,1,""],lexer:[5,7,1,""],t_COMMENT:[5,4,1,""],t_ID:[5,4,1,""],t_error:[5,4,1,""],t_newline:[5,4,1,""]},"pype.lib_import":{LibraryImporter:[5,2,1,""],component:[5,4,1,""],is_component:[5,4,1,""]},"pype.lib_import.LibraryImporter":{add_symbols:[5,1,1,""],import_module:[5,1,1,""]},"pype.optimize":{AssignmentEllision:[5,2,1,""],DeadCodeElimination:[5,2,1,""],FlowgraphOptimization:[5,2,1,""],InlineComponents:[5,2,1,""],NodeOptimization:[5,2,1,""],Optimization:[5,2,1,""],PrintIR:[5,2,1,""],TopologicalFlowgraphOptimization:[5,2,1,""],TopologicalNodeOptimization:[5,2,1,""]},"pype.optimize.AssignmentEllision":{visit:[5,1,1,""]},"pype.optimize.DeadCodeElimination":{visit:[5,1,1,""]},"pype.optimize.InlineComponents":{visit:[5,1,1,""]},"pype.optimize.Optimization":{visit:[5,1,1,""]},"pype.optimize.PrintIR":{visit:[5,1,1,""]},"pype.parser":{p_assign:[5,4,1,""],p_component:[5,4,1,""],p_declaration:[5,4,1,""],p_declaration_list:[5,4,1,""],p_error:[5,4,1,""],p_expression_list:[5,4,1,""],p_functioncall:[5,4,1,""],p_identification:[5,4,1,""],p_import_statement:[5,4,1,""],p_input:[5,4,1,""],p_literal:[5,4,1,""],p_op_add_expression:[5,4,1,""],p_op_div_expression:[5,4,1,""],p_op_mul_expression:[5,4,1,""],p_op_sub_expression:[5,4,1,""],p_output:[5,4,1,""],p_parameter_list:[5,4,1,""],p_program:[5,4,1,""],p_statement_list:[5,4,1,""],p_type:[5,4,1,""]},"pype.pcode":{PCode:[5,2,1,""],PCodeGenerator:[5,2,1,""],PCodeOp:[5,2,1,""]},"pype.pcode.PCode":{add_op:[5,1,1,""],driver:[5,1,1,""],input_generator:[5,1,1,""],output_collector:[5,1,1,""],run:[5,1,1,""]},"pype.pcode.PCodeGenerator":{visit:[5,1,1,""]},"pype.pcode.PCodeOp":{forward:[5,6,1,""],input:[5,6,1,""],libraryfunction:[5,6,1,""],librarymethod:[5,6,1,""],literal:[5,6,1,""]},"pype.pipeline":{Pipeline:[5,2,1,""]},"pype.pipeline.Pipeline":{compile:[5,1,1,""],optimize:[5,1,1,""],optimize_AssignmentEllision:[5,1,1,""],optimize_DeadCodeElimination:[5,1,1,""]},"pype.semantic_analysis":{CheckSingleAssignment:[5,2,1,""],CheckSingleIOExpression:[5,2,1,""],CheckUndefinedVariables:[5,2,1,""],PrettyPrint:[5,2,1,""]},"pype.semantic_analysis.CheckSingleAssignment":{visit:[5,1,1,""]},"pype.semantic_analysis.CheckSingleIOExpression":{visit:[5,1,1,""]},"pype.semantic_analysis.CheckUndefinedVariables":{visit:[5,1,1,""]},"pype.semantic_analysis.PrettyPrint":{visit:[5,1,1,""]},"pype.symtab":{Symbol:[5,2,1,""],SymbolTable:[5,2,1,""],SymbolType:[5,2,1,""]},"pype.symtab.Symbol":{"__getnewargs__":[5,1,1,""],"__new__":[5,6,1,""],"__repr__":[5,1,1,""],name:[5,3,1,""],ref:[5,3,1,""],type:[5,3,1,""]},"pype.symtab.SymbolTable":{addsym:[5,1,1,""],lookupsym:[5,1,1,""],pprint:[5,1,1,""],scopes:[5,1,1,""]},"pype.symtab.SymbolType":{"var":[5,3,1,""],component:[5,3,1,""],input:[5,3,1,""],libraryfunction:[5,3,1,""],librarymethod:[5,3,1,""],output:[5,3,1,""]},"pype.translate":{LoweringVisitor:[5,2,1,""],SymbolTableVisitor:[5,2,1,""]},"pype.translate.LoweringVisitor":{post_visit:[5,1,1,""],visit:[5,1,1,""]},"pype.translate.SymbolTableVisitor":{return_value:[5,1,1,""],visit:[5,1,1,""]},"timeseries.TimeSeries":{TimeSeries:[6,2,1,""]},"timeseries.TimeSeries.TimeSeries":{"__contains__":[6,1,1,""],"__getitem__":[6,1,1,""],"__iter__":[6,1,1,""],"__len__":[6,1,1,""],"__radd__":[6,1,1,""],"__repr__":[6,1,1,""],"__rmul__":[6,1,1,""],"__rsub__":[6,1,1,""],"__setitem__":[6,1,1,""],"__str__":[6,1,1,""],from_json:[6,5,1,""],interpolate:[6,1,1,""],items:[6,3,1,""],iteritems:[6,1,1,""],itertimes:[6,1,1,""],itervalues:[6,1,1,""],mean:[6,1,1,""],median:[6,1,1,""],std:[6,1,1,""],times:[6,3,1,""],to_json:[6,1,1,""],values:[6,3,1,""]},"tsdb.baseclasses":{BaseDB:[7,2,1,""],BaseIndex:[7,2,1,""]},"tsdb.baseclasses.BaseDB":{"__getitem__":[7,1,1,""],delete_ts:[7,1,1,""],insert_ts:[7,1,1,""],select:[7,1,1,""],upsert_meta:[7,1,1,""]},"tsdb.baseclasses.BaseIndex":{getEqual:[7,1,1,""],insert:[7,1,1,""],remove:[7,1,1,""]},"tsdb.dictdb":{DictDB:[7,2,1,""]},"tsdb.dictdb.DictDB":{"__getitem__":[7,1,1,""],delete_ts:[7,1,1,""],index_bulk:[7,1,1,""],indexes:[7,3,1,""],insert_ts:[7,1,1,""],pkfield:[7,3,1,""],remove_from_indices:[7,1,1,""],rows:[7,3,1,""],schema:[7,3,1,""],select:[7,1,1,""],ts_length:[7,3,1,""],update_indices:[7,1,1,""],upsert_meta:[7,1,1,""]},"tsdb.heap":{HeapFile:[7,2,1,""],MetaHeapFile:[7,2,1,""],TSHeapFile:[7,2,1,""]},"tsdb.heap.HeapFile":{close:[7,1,1,""]},"tsdb.heap.MetaHeapFile":{check_byteArray:[7,1,1,""],encode_and_write_meta:[7,1,1,""],read_and_return_meta:[7,1,1,""]},"tsdb.heap.TSHeapFile":{encode_and_write_ts:[7,1,1,""],read_and_decode_ts:[7,1,1,""]},"tsdb.indices":{BitmapIndex:[7,2,1,""],PKIndex:[7,2,1,""],SimpleIndex:[7,2,1,""],TreeIndex:[7,2,1,""]},"tsdb.indices.BitmapIndex":{allKeys:[7,1,1,""],deleteIndex:[7,1,1,""],get:[7,1,1,""],getEqual:[7,1,1,""],getNotEq:[7,1,1,""],insert:[7,1,1,""],remove:[7,1,1,""]},"tsdb.indices.PKIndex":{close:[7,1,1,""],getEqual:[7,1,1,""],insert:[7,1,1,""],keys:[7,1,1,""],load_and_clear_log:[7,1,1,""],load_pickle:[7,1,1,""],remove:[7,1,1,""],save_pickle:[7,1,1,""]},"tsdb.indices.SimpleIndex":{getEqual:[7,1,1,""],insert:[7,1,1,""],remove:[7,1,1,""]},"tsdb.indices.TreeIndex":{allKeys:[7,1,1,""],deleteIndex:[7,1,1,""],get:[7,1,1,""],getEqual:[7,1,1,""],getHigherOrEq:[7,1,1,""],getHigherThan:[7,1,1,""],getLowerOrEq:[7,1,1,""],getLowerThan:[7,1,1,""],getNotEq:[7,1,1,""],insert:[7,1,1,""],remove:[7,1,1,""]},"tsdb.persistentdb":{PersistentDB:[7,2,1,""],dict_eq:[7,4,1,""]},"tsdb.persistentdb.PersistentDB":{"__getitem__":[7,1,1,""],"__len__":[7,1,1,""],add_vp:[7,1,1,""],close:[7,1,1,""],delete_database:[7,1,1,""],delete_ts:[7,1,1,""],delete_vp:[7,1,1,""],index_bulk:[7,1,1,""],insert_ts:[7,1,1,""],load_vps:[7,1,1,""],remove_indices:[7,1,1,""],select:[7,1,1,""],update_indices:[7,1,1,""],upsert_meta:[7,1,1,""]},"tsdb.tsdb_client":{TSDBClient:[7,2,1,""]},"tsdb.tsdb_client.TSDBClient":{add_trigger:[7,1,1,""],augmented_select:[7,1,1,""],delete_ts:[7,1,1,""],find_similar:[7,1,1,""],insert_ts:[7,1,1,""],make_vp_tree:[7,1,1,""],port:[7,3,1,""],remove_trigger:[7,1,1,""],select:[7,1,1,""],upsert_meta:[7,1,1,""]},"tsdb.tsdb_error":{TSDBStatus:[7,2,1,""]},"tsdb.tsdb_error.TSDBStatus":{INVALID_KEY:[7,3,1,""],INVALID_OPERATION:[7,3,1,""],OK:[7,3,1,""],UNKNOWN_ERROR:[7,3,1,""],encode:[7,1,1,""],encoded_length:[7,6,1,""],from_bytes:[7,5,1,""]},"tsdb.tsdb_ops":{TSDBOp:[7,2,1,""],TSDBOp_AddTrigger:[7,2,1,""],TSDBOp_AugmentedSelect:[7,2,1,""],TSDBOp_DeleteTS:[7,2,1,""],TSDBOp_FindSimilar:[7,2,1,""],TSDBOp_InsertTS:[7,2,1,""],TSDBOp_MakeVPTree:[7,2,1,""],TSDBOp_RemoveTrigger:[7,2,1,""],TSDBOp_Return:[7,2,1,""],TSDBOp_Select:[7,2,1,""],TSDBOp_UpsertMeta:[7,2,1,""]},"tsdb.tsdb_ops.TSDBOp":{from_json:[7,5,1,""],to_json:[7,1,1,""]},"tsdb.tsdb_ops.TSDBOp_AddTrigger":{from_json:[7,5,1,""]},"tsdb.tsdb_ops.TSDBOp_AugmentedSelect":{from_json:[7,5,1,""]},"tsdb.tsdb_ops.TSDBOp_DeleteTS":{from_json:[7,5,1,""]},"tsdb.tsdb_ops.TSDBOp_FindSimilar":{from_json:[7,5,1,""]},"tsdb.tsdb_ops.TSDBOp_InsertTS":{from_json:[7,5,1,""]},"tsdb.tsdb_ops.TSDBOp_MakeVPTree":{from_json:[7,5,1,""]},"tsdb.tsdb_ops.TSDBOp_RemoveTrigger":{from_json:[7,5,1,""]},"tsdb.tsdb_ops.TSDBOp_Return":{from_json:[7,5,1,""]},"tsdb.tsdb_ops.TSDBOp_Select":{from_json:[7,5,1,""]},"tsdb.tsdb_ops.TSDBOp_UpsertMeta":{from_json:[7,5,1,""]},"tsdb.tsdb_serialization":{Deserializer:[7,2,1,""],serialize:[7,4,1,""]},"tsdb.tsdb_serialization.Deserializer":{append:[7,1,1,""],deserialize:[7,1,1,""],ready:[7,1,1,""]},"tsdb.tsdb_server":{TSDBProtocol:[7,2,1,""],TSDBServer:[7,2,1,""],trigger_callback_maker:[7,4,1,""]},"tsdb.tsdb_server.TSDBProtocol":{connection_lost:[7,1,1,""],connection_made:[7,1,1,""],data_received:[7,1,1,""]},"tsdb.tsdb_server.TSDBServer":{db:[7,3,1,""],exception_handler:[7,1,1,""],port:[7,3,1,""],run:[7,1,1,""],triggers:[7,3,1,""]},"vptrees.vptrees":{VPNode:[8,2,1,""],VPTree:[8,2,1,""],VPTreeLeaf:[8,2,1,""],VPTreeNonLeaf:[8,2,1,""]},"vptrees.vptrees.VPNode":{preorder:[8,1,1,""]},"vptrees.vptrees.VPTree":{dot:[8,1,1,""],getCloseSubset:[8,1,1,""],makeVPTree:[8,1,1,""]},"webserver.web_server":{Handlers:[9,2,1,""],WebServer:[9,2,1,""]},"webserver.web_server.Handlers":{add_metadata_handler:[9,1,1,""],add_trigger_handler:[9,1,1,""],add_ts_handler:[9,1,1,""],augselect_handler:[9,1,1,""],delete_ts_handler:[9,1,1,""],find_similar_handler:[9,1,1,""],homepage_handler:[9,1,1,""],make_vp_tree_handler:[9,1,1,""],remove_trigger_handler:[9,1,1,""],select_handler:[9,1,1,""]},"webserver.web_server.WebServer":{app:[9,3,1,""],handler:[9,3,1,""],run:[9,1,1,""]},"webutils.webclient":{WebClient:[10,2,1,""]},"webutils.webclient.WebClient":{add_trigger:[10,1,1,""],augselect:[10,1,1,""],delete_ts:[10,1,1,""],find_similar:[10,1,1,""],homepage:[10,1,1,""],insert_ts:[10,1,1,""],make_vp_tree:[10,1,1,""],remove_trigger:[10,1,1,""],select:[10,1,1,""],upsert_meta:[10,1,1,""]},go_server:{identity:[0,4,1,""],main:[0,4,1,""],to_bool:[0,4,1,""],to_float:[0,4,1,""],to_int:[0,4,1,""]},go_server_persistent:{main:[1,4,1,""]},go_webserver:{main:[2,4,1,""]},procs:{corr:[4,0,0,"-"],junk:[4,0,0,"-"],stats:[4,0,0,"-"]},pype:{ast:[5,0,0,"-"],error:[5,0,0,"-"],fgir:[5,0,0,"-"],lexer:[5,0,0,"-"],lextab:[5,0,0,"-"],lib_import:[5,0,0,"-"],optimize:[5,0,0,"-"],parser:[5,0,0,"-"],parsetab:[5,0,0,"-"],pcode:[5,0,0,"-"],pipeline:[5,0,0,"-"],semantic_analysis:[5,0,0,"-"],symtab:[5,0,0,"-"],translate:[5,0,0,"-"]},timeseries:{TimeSeries:[6,0,0,"-"]},tsdb:{baseclasses:[7,0,0,"-"],dictdb:[7,0,0,"-"],heap:[7,0,0,"-"],indices:[7,0,0,"-"],persistentdb:[7,0,0,"-"],tsdb_client:[7,0,0,"-"],tsdb_error:[7,0,0,"-"],tsdb_ops:[7,0,0,"-"],tsdb_serialization:[7,0,0,"-"],tsdb_server:[7,0,0,"-"]},vptrees:{vptrees:[8,0,0,"-"]},webserver:{web_server:[9,0,0,"-"]},webutils:{webclient:[10,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","method","Python method"],"2":["py","class","Python class"],"3":["py","attribute","Python attribute"],"4":["py","function","Python function"],"5":["py","classmethod","Python class method"],"6":["py","staticmethod","Python static method"],"7":["py","data","Python data"],"8":["py","exception","Python exception"]},objtypes:{"0":"py:module","1":"py:method","2":"py:class","3":"py:attribute","4":"py:function","5":"py:classmethod","6":"py:staticmethod","7":"py:data","8":"py:exception"},terms:{"__abs__":[],"__add__":6,"__bool__":[],"__contains__":6,"__get_index":[],"__getitem__":[6,7],"__getnewargs__":5,"__init__":[],"__iter__":6,"__len__":[6,7],"__mul__":6,"__neg__":[],"__new__":5,"__pos__":[],"__radd__":6,"__repr__":[5,6],"__rmul__":6,"__rsub__":6,"__setitem__":6,"__str__":6,"__sub__":6,"__truediv__":[],"_cl":5,"_corr":4,"break":[0,1,2,5],"byte":7,"case":4,"class":[5,6,7,8,9,10],"default":[2,5,7,9],"enum":[5,7],"function":[4,5,6,7,8],"import":5,"int":[4,7],"long":7,"new":[5,7,13],"return":[4,5,6,7,8,9,13],"static":[5,7],"true":[5,7],"try":9,"var":5,"while":5,accept:[5,7],access:5,add:[5,7,9,13],add_input:5,add_metadata_handl:9,add_op:5,add_output:5,add_symbol:5,add_trigg:[7,10,13],add_trigger_handl:9,add_ts_handl:9,add_vp:7,addit:[6,7,9,10,13],addsym:5,adjch:13,affect:5,after:[5,7,9],ahead:7,aiotttp:9,akhil:[11,14],akhilketkar:11,alia:5,all:[5,7,9],allkei:7,allow:[5,7],alongsid:5,also:[0,1,2,5,7],analysi:5,analyz:5,ani:[5,7],anoth:4,anyth:[4,8],app:9,append:7,appli:5,applic:9,appropri:7,arbitrari:7,arg:[4,5,7,8,9,10,13],argument:[0,1,4,5,7,8,9],arguments_list:5,arrai:6,ask:[],assert:13,assign:5,assignmentellis:5,associ:7,assum:7,assur:7,ast:[],astassignmentexpr:5,astcompon:5,astevalexpr:5,astid:5,astimport:5,astinputexpr:5,astliter:5,astmodvisitor:5,astnod:5,astoutputexpr:5,astprogram:5,astvisitor:5,async:9,asyncio:7,attempt:7,attribut:5,augmented_select:7,augselect:[10,13],augselect_handl:9,avail:9,avl:7,back:7,backend:7,base:[0,5,6,7,8,9,10],baseclass:[],basedb:7,baseindex:[],been:13,befor:[5,7],between:[4,8],binari:7,bind:5,bitmap:7,bitmapindex:7,bitmask:7,block:5,bool:[],bool_arrai:[],bool_to_str:[],buffer:7,bug:[],build:5,bytearrai:7,calcul:6,call:[4,5,7,9,13],calltomak:7,can:[5,7,8,13],candid:8,cannot:5,cardin:7,chang:[5,7],charact:5,check:[5,7],check_bytearrai:7,checksingleassign:5,checksingleioexpress:5,checkundefinedvari:5,child:5,child_valu:5,children:5,christian:11,chunk:7,classmethod:[6,7],clear:7,client:7,close:7,closest:[7,8,9],code:[0,1,2,5],collect:6,column:[5,7],column_nam:4,com:11,comment:5,commun:7,compat:5,compil:5,compon:5,component1:5,component2:5,compress:7,comput:[4,5,7],conn:7,connect:[5,7],connection_lost:7,connection_mad:7,consid:7,consist:[4,6],construct:5,contain:[7,8,9],content:[],context:7,convert:[],copi:5,copyright:14,coroutin:5,corr:[],correct:9,correl:4,correspond:9,could:[5,7],creat:[5,8],criteria:[7,9],current:[7,13],currentlli:7,d_vp:9,daniel:11,data:[5,6,7,13],data_receiv:7,databas:[0,1,4,7,9,13],database_nam:7,datalist:6,date:7,db_name:7,dce:5,dead:5,deadcodeelimin:5,debug:5,declar:5,declaration_list:5,decor:5,def:[],defin:[7,9],deleg:[6,7],delet:[5,7,9],delete_databas:7,delete_t:[7,10],delete_ts_handl:9,delete_vp:7,deleteindex:7,demo:[0,1,2,13],depend:5,depth:5,describ:9,descriptor:7,deseri:7,desir:5,detail:[9,13],detect:7,dev:[],deviat:4,dict1:7,dict2:7,dict:[4,5,7],dict_eq:7,dictdb:[],dictionari:[0,4,7,9],differ:5,disk:7,dispatch:7,dist_arg:8,dist_func:8,distanc:[4,7,8],divid:[],divis:[],dny:5,doe:[4,5],done:[4,7],dot:8,dotfil:5,doubl:7,driver:5,dump:[],dunder:[6,7],duplic:7,each:[5,6,7],edit:[0,1,2],effect:5,either:7,element:[5,7],elementwis:[],elimin:5,elsewher:7,empti:[],encaplu:7,encod:[7,9],encode_and_write_meta:7,encode_and_write_t:7,encoded_length:7,encount:7,end:[5,7,13],endpoint:[9,10,13],engin:7,entri:7,enumer:5,equal:7,error:[],essenti:7,establish:7,event:[9,13],everi:5,everyth:7,exampl:[0,1,2,5,13],except:[5,7],exception_handl:7,execut:5,exist:9,explicit:5,expos:[5,10],express:5,expression_list:5,extens:5,failur:9,fals:[5,7],fast:13,featur:[],fgir:[],fgnode:5,fgnodetyp:5,field:[5,7,9,10],fieldnam:7,fields_to_ret:7,fieldvalu:7,file:[0,1,2,5,7,8],filter:7,find:[],find_column:5,find_similar:[7,10,13],find_similar_handl:9,first:5,fix:7,flow:5,flowgraph:5,flowgraph_optim:5,flowgraph_pass:5,flowgraphoptim:5,focus:5,follow:7,form:4,format:[5,13],forward:5,found:5,four:7,from:[5,7,13],from_byt:7,from_json:[6,7],full:[7,13],func:5,funciton:[],function_ref:5,futur:5,gener:5,get:[7,8,9,13],get_var:5,getclosesubset:8,getequ:7,gethigheroreq:7,gethigherthan:7,getloweroreq:7,getlowerthan:7,getnoteq:7,give:[5,6],given:[0,1,4,5,6,7],global:5,gmail:11,graph:5,graphviz:8,guarante:5,handl:[6,9],handler:9,hasattr:[],heap:[],heap_file_nam:7,heapfil:7,help:5,helper:7,here:7,hilawi:11,hnadler:9,homepag:[9,10],homepage_handl:9,how:[0,1,2],howev:5,http:13,hybrid:7,ident:0,identifi:7,idnam:5,ignor:[4,5,7,9],illeg:5,imagin:5,implement:[4,5,6,7,9,13],import_modul:5,import_stat:5,in_q:5,includ:7,indent:5,index:[7,13],index_bulk:7,indic:[],info:9,inform:[9,13],injest:5,inlin:5,inlinecompon:5,input:5,input_arg:5,input_gener:5,insert:[],insert_t:[7,10,13],instanc:[5,7],instanti:[],instead:7,intenum:7,interact:10,interfac:[5,7],intermedi:5,interpol:6,invalid:7,invalid_kei:7,invalid_oper:7,invoc:5,invok:5,is_compon:5,item:6,iter:6,iteritem:6,itertim:6,itervalu:6,itself:5,json:[7,9,13],json_dict:7,json_obj:7,json_text:13,juaquin:11,junk:[],just:9,keep:5,kei:[4,5,7,8,9,13],kerndist:4,kernel:4,ketkar:14,keyword:5,label:7,lai:[],lbrace:5,left_child:8,len:[0,1,13],lenght:7,length:[0,1,6,7],level:5,lex:5,lexer:[],lextab:[],lib_import:[],libraryfunct:5,libraryimport:5,librarymethod:5,like:7,limit:[7,13],line:5,list:[4,5,6,7,8,9],liter:5,load:7,load_and_clear_log:7,load_pickl:7,load_vp:7,localhost:13,locat:5,log:7,logic:7,longer:5,look:5,lookupsym:5,loop:7,lot:6,low:7,lower:5,loweringvisitor:5,lparen:5,made:13,magnitud:6,mai:5,main:[0,1,2,4],make:9,make_add_trigg:[],make_insert_t:[],make_upsert_meta:[],make_vp_tre:[7,10,13],make_vp_tree_handl:9,makevptre:8,manupil:6,mark:5,match:[7,9],mean:[4,6],meant:[0,1,2],median:6,median_dist:8,memori:[0,7],meta1:[],meta:7,metadata:[],metadata_dict:[7,9,10],metadict:13,metaheapfil:7,method:[5,6,7],method_ref:5,metric:[4,7],might:[0,1,2,5],minu:[],miss:7,mod_visitor:5,mod_walk:5,modifi:5,modnam:5,more:5,most:[7,13],msg:5,multipl:[5,6],multipli:[],must:9,name:[5,7,9],nasti:[],necessari:5,need:7,negat:[],network:7,never:5,new_meta:7,new_nod:5,newlin:5,nice:5,nid:5,node:[5,8],node_optim:5,node_pass:5,nodeid:5,nodeoptim:5,nodes_left:5,nodetyp:5,none:[4,5,7,8,10,13],norm:[],normal:5,note:[],noth:[4,5],number:[0,1,5,7],obj:[5,7],object:[5,6,7,8,9,10,13],observ:6,occur:[7,13],odl:[],off:7,offer:5,offset:7,okai:7,old:7,old_meta_dict:7,onli:[0,1,2,5,7],onwhat:[7,9,10],op_add:5,op_div:5,op_mul:5,op_sub:5,open:7,oper:[5,7],operator_num:7,optim:[],optimize_assignmentellis:5,optimize_deadcodeelimin:5,optin:9,option:[4,7],order:[5,9],org:13,origin:5,other:[5,7],otherwis:7,our:[0,1,2,9,13],out:[5,7],out_q:5,output:[5,9],output_collector:5,over:6,own:7,p_assign:5,p_compon:5,p_declar:5,p_declaration_list:5,p_error:5,p_expression_list:5,p_functioncal:5,p_identif:5,p_import_stat:5,p_input:5,p_liter:5,p_op_add_express:5,p_op_div_express:5,p_op_mul_express:5,p_op_sub_express:5,p_output:5,p_parameter_list:5,p_program:5,p_statement_list:5,p_type:5,packag:[],page:13,pair:7,param:[],paramet:[4,7,8,9,13],parameter_list:5,parent:5,parser:[],parsetab:[],particular:13,pass:[4,5,7],payload:7,pcode:[],pcode_op_coroutin:5,pcodegener:5,pcodeop:5,perform:[5,7,13],persist:[1,7],persistantdb:[],persistentdb:[],pickl:[5,7],pipelin:[],pk_field:7,pk_len:[],pk_list:8,pk_offset:7,pkfield:7,pkindex:7,place:7,plain:5,ply:5,point:[0,1,6,7,8,9,13],port:7,possibl:[7,8],post:[5,13],post_visit:5,postvisit:5,pprint:5,pre:5,predefin:[7,9,13],preorder:8,prettyprint:5,primari:[4,7,8,9],primary_kei:[7,9,10,13],print:5,printir:5,proc:[],proc_main:4,procedur:[4,7,9,13],process:7,produc:5,product:[],program:[5,7],programm:[5,6],project:13,protocol:7,provid:6,pull:7,pype:[],pypesyntaxerror:5,pypetypeerror:5,pyscaffold:13,python:[7,13],queri:[7,8,9,13],queryt:[],rais:[],rbrace:5,read:5,read_and_decode_t:7,read_and_return_meta:7,readi:7,readthedoc:13,receiv:7,recent:[],recommn:13,reconstruct:7,record:6,recurs:5,ref:5,refer:[4,7,9],regular:13,remov:[],remove_from_indic:7,remove_indic:7,remove_trigg:[7,10,13],remove_trigger_handl:9,repl:7,replac:5,report:7,repres:[5,8],represent:[5,6],request:[7,9,10,13],requir:9,reserv:5,respons:[7,9,13],rest:[9,13],result:[5,7,9],return_valu:5,reus:5,right_child:8,row:[4,7,9,13],rparen:5,rule:5,run:[5,7,9,13],safe:5,same:[],save:7,save_pickl:7,schema:7,scope:5,search:13,see:13,seem:5,select:[],select_handl:9,self:5,semant:5,semantic_analysi:[],send:7,sent:[7,9],serach:13,seri:[6,7,9,13],serial:7,server:[0,1,2,7,9,13],server_url:10,set:[2,6,7,13],set_var:5,shorten:6,should:[5,7,9],shove:7,show:9,shown:5,sibl:5,signatur:5,similar:[],similarli:13,simpl:[5,7],simpleindex:7,simpli:5,simplifi:7,sinc:5,singl:5,skip:5,some:[2,5,9],sort:[5,7],sort_bi:13,sourc:5,spit:5,standard:4,start:[0,1,2,13],stat:[],state:[7,13],statement:5,statement_list:5,statu:7,status:7,status_cod:13,std:6,storag:7,store:[4,7,9,13],str_to_bool:[],string:[4,5,6,7],string_lin:[],structur:7,subclass:[],submit:[6,7],submodul:[],subset:8,subtract:6,succeed:7,success:9,suitabl:7,sum:[],support:[7,10,13],sure:5,sym:5,symbol:5,symbolt:5,symboltablevisitor:5,symboltyp:5,symtab:[],system:[0,1,2],t_comment:5,t_error:5,t_id:5,t_newlin:5,take:[0,1,7,8],talk:[9,10,13],target:[7,9,10],test:[0,1,2,4,5,7],test_persistantdb:[],text:[5,9,13],than:5,thei:[5,7],them:[5,7,8],thi:[0,1,2,4,5,7,8,9,13],those:6,through:7,time1:6,time2:6,time:[5,6,7,9,13],timeseri:[],timeslist:6,to_bool:0,to_float:0,to_int:0,to_json:[6,7],tok:5,token:5,top:5,topo_flowgraph_optim:5,topo_optim:5,topo_sort:5,topo_visitnod:5,topo_vistnod:5,topolog:5,topological_flowgraph_pass:5,topological_node_pass:5,topological_sort:5,topologicalflowgraphoptim:5,topologicalnodeoptim:5,track:5,transform:5,translat:[],transport:7,travers:5,tree:9,treeindex:7,trigger:[],trigger_callback_mak:7,truth:6,ts1:[],ts_length:7,tsdb:[],tsdb_client:[],tsdb_error:[],tsdb_op:[],tsdb_serial:[],tsdb_server:[],tsdbclient:7,tsdbop:7,tsdbop_addtrigg:7,tsdbop_augmentedselect:7,tsdbop_deletet:7,tsdbop_findsimilar:7,tsdbop_insertt:7,tsdbop_makevptre:7,tsdbop_removetrigg:7,tsdbop_return:7,tsdbop_select:7,tsdbop_upsertmeta:7,tsdbprotocol:7,tsdbserver:7,tsdbstatu:7,tsheapfil:7,tsmaker:[],tupl:[5,6],turn:7,two:[0,1,5],type:[4,5,7,9],typedecl:5,uid:8,uniqu:7,unknown:[5,7],unknown_error:7,unmodifi:5,unreach:5,until:7,updat:[5,7,13],update_indic:7,upsert:[],upsert_meta:[7,10,13],url:13,useless:5,user:[5,7,10],utilit:10,valid:5,valu:[4,5,6,7],value1:6,value2:6,value_ref:5,valueerror:[],vantag:[0,1,7,8,9,13],variabl:[5,7],varibl:9,variou:9,verb:13,veri:7,via:[7,10],visit:5,visit_valu:5,visitor:5,visual:8,vp_id:7,vp_kei:8,vp_pk:8,vpkei:9,vpnode:8,vptree:[],vptreeleaf:8,vptreenonleaf:8,wai:[0,1,2,7],walk:5,want:9,warn:5,web:[2,7,9,13],web_serv:[],webclient:[],webserv:[],websev:10,webutil:[],were:6,what:[7,9],when:[5,13],where:[9,10],where_dict:13,whether:5,which:[4,5,7,9],who:[],width:7,wire:7,within:6,work:[],would:5,wrapper:7,write:[7,9],writelog:7,www:13,you:[0,1,2,5,7],your:[],z_0:[]},titles:["go_server module","go_server_persistent module","go_webserver module","Modules","procs package","pype package","timeseries package","tsdb package","vptrees package","webserver package","webutils package","Developers","Changelog","TimeSeries Utility","License"],titleterms:{api:13,ast:5,augment:13,baseclass:7,baseindex:[],changelog:12,content:[4,5,6,7,8,9,10],corr:4,cs207project:[],descript:13,develop:11,dictdb:7,document:[],error:5,fgir:5,find:13,go_serv:0,go_server_persist:1,go_webserv:2,guid:13,heap:7,iii:13,indic:7,insert:13,junk:4,lexer:5,lextab:5,lib_import:5,licens:14,make:13,metadata:13,modul:[0,1,2,3,4,5,6,7,8,9,10],note:13,optim:5,packag:[4,5,6,7,8,9,10],parser:5,parsetab:5,pcode:5,persistantdb:[],persistentdb:7,pipelin:5,proc:4,pype:5,quick:13,remov:13,select:13,semantic_analysi:5,setup:13,similar:13,stat:4,submodul:[4,5,6,7,8,9,10],symtab:5,tabl:[],team:[],test_persistantdb:[],timeseri:[6,13],translat:5,tree:13,trigger:13,tsdb:7,tsdb_client:7,tsdb_error:7,tsdb_op:7,tsdb_serial:7,tsdb_server:7,upsert:13,usag:13,util:13,version:12,vii:13,vptree:8,web_serv:9,webclient:10,webserv:9,webutil:10,welcom:[]}})