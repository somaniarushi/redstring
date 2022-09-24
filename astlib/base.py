import os
import ast
from loguru import logger
from pathlib import Path

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
            self.prg_ast = ast.parse(prg_str)
        except SyntaxError as _:
            raise PrgASTError(f"Could not parse into AST: {prg_str}")

    @classmethod
    def from_string(cls, string):
        return PrgAST(string)

    @classmethod
    def from_file(cls, filepath):
        curr_dir = Path(__file__).parent
        sanitized_path = (curr_dir / filepath).resolve()
        if os.path.exists(sanitized_path):
            pass
        else:
            raise PrgASTError(f"Filepath could not be located: {filepath}")
