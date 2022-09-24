import ast
from gen.gen import *

def is_def_in_scope(call_node, func_def_node):
    call_parent = call_node.parent
    func_def_node_parent = func_def_node.parent
    while call_parent.parent is not None:
        if func_def_node_parent == call_parent:
            return True
        call_parent = call_parent.parent
    return False

def is_func_defined_in_scope(prg_str, func_name):
    ast_nodes = ast.parse(prg_str)
    root_of_ast = add_parent_tracking(ast_nodes)
    call_node = get_func_call_in_ast(root_of_ast, func_name)
    if call_node is None:
        return False
    func_def_node = get_func_def_in_ast(root_of_ast, func_name)
    if func_def_node is None:
        return False
    in_scope = is_def_in_scope(call_node, func_def_node)
    return is_scope