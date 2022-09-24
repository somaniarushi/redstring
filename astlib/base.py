import os
import sys
import ast
import astpretty
from loguru import logger
import ast_scope
from utils import sanitize_for_root

class Parentage(ast.NodeTransformer):
    parent = None

    def visit(self, node):
        node.parent = self.parent
        self.parent = node
        node = super().visit(node)
        if isinstance(node, ast.AST):
            self.parent = node.parent
        return node


class PrgASTError(SyntaxError):
    """
    An internal error with AST manipulation
    """
    def __init__(self, msg):
        logger.error(msg)
        super().__init__(msg)

class PrgAST:
    """
    The PrgAST is an AST representation of any given program.
    Here, a program represents a RedString file. This AST can be initialized
    through various methods:
    1. Accepting a string representation of the program
    2. Accepting a path to the file containing the program
    3. Accepting a Python AST representation of the program
    """
    def __init__(self, prg_str: str):
        self.prg_str = prg_str
        try:
            self.prg_ast = Parentage().visit(ast.parse(prg_str))
            self.prg_ast_scope = ast_scope.annotate(self.prg_ast)
        except SyntaxError as _:
            raise PrgASTError(f"Could not parse into AST: {prg_str}")

    @classmethod
    def from_string(cls, string: str):
        return PrgAST(string)

    @classmethod
    def from_file(cls, filepath: str):
        sanitized_path = sanitize_for_root(filepath)
        if os.path.exists(sanitized_path):
            with open(sanitized_path) as f:
                prg_str = f.read()
                return PrgAST(prg_str)
        else:
            raise PrgASTError(f"Filepath could not be located: {filepath}")

    @classmethod
    def from_ast(cls, prg_ast: ast.AST):
        return PrgAST(ast.unparse(prg_ast))

    def get_module_stmts(self):
        """
        Returns a list of the statements that compose the body of the AST.
        """
        return self.prg_ast.body

    def get_statements(self):
        """
        Returns every statement in the body of the AST.
        """
        return ast.walk(self.prg_ast)

    def get_scope_dict(self):
        return self.prg_ast_scope

    def get_scope_info(self, node):
        assert node in self.get_statements(), 'node must be in program'
        return self.prg_ast_scope[node]

    def __repr__(self):
        return self.prg_str

    def __str__(self):
        return astpretty.pformat(self.prg_ast)


if __name__ == "__main__":
    """
    Minimal testing bench
    """
    args = sys.argv[1:]
    test_string = True if len(args) < 1 else args[0]
    test_file = True if len(args) < 2 else args[1]

    if test_string:
        print(PrgAST.from_string("lambda x: x + 1"))
    if test_file:
        print(PrgAST.from_file("tests/test_files/parse_simple.py"))
