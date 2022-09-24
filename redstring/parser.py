"""
This file contains RedString specific functions only.
"""
import astpretty

from astlib.base import PrgAST
from loguru import logger
import ast

def is_def_in_scope(call_node, func_def_node):
    call_node_parent = call_node.parent
    func_def_node_parent = func_def_node.parent
    while call_node_parent is not None:
        if call_node_parent == func_def_node_parent:
            return True
        call_node_parent = call_node_parent.parent
    return False


def get_undefined_functions(prg: PrgAST):
    """
    Returns all the undefined functions, that the tool then has the objective of describing.
    :param prg: An AST that contains function declarations
    :return: A list of function call objects for which the function is not defined
    """
    statements = prg.get_statements()
    func_defs = []
    func_def_names = []
    for stmt in statements:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if stmt.name not in func_def_names:
                func_defs.append(stmt)
                func_def_names.append(stmt.name)
    try:
        func_def_names.extend(list(__builtins__))
        # func_defs.extend(list(__builtins__))
    except TypeError as e:
        logger.warning("Could not add builtins to defined functions list")

    ast_nodes = prg.get_statements()
    undefined_fn_calls = []
    undefined_fn_names = []
    for node in ast_nodes:
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                name = node.func.id
                if name in undefined_fn_names:
                    continue

                # If function has never been defined, add
                if name not in func_def_names:
                    undefined_fn_calls.append(node)
                    undefined_fn_names.append(name)

                # If it is defined, check if the scope is correct
                if name in func_def_names:
                    idx = func_def_names.index(name)
                    if idx >= len(func_defs):  # It is a builtin
                        continue

                    func_def = func_defs[idx]
                    if not is_def_in_scope(node, func_def):
                        undefined_fn_calls.append(node)
                        undefined_fn_names.append(name)

    logger.info(f"Found undefined functions: {undefined_fn_names}")
    return undefined_fn_calls


if __name__ == "__main__":
    prg = PrgAST.from_file('tests/test_files/test_undefined.py')
    # print(prg)
    get_undefined_functions(prg)