import fire
from astlib.base import PrgAST
from redstring.synthesize import get_generated_functions
from loguru import logger
from utils import sanitize_for_root, get_json_from_file

def generate(in_path, out_path='gen/gen.py'):
    prg = PrgAST.from_file(in_path)
    functions = get_generated_functions(prg)

    out_sanitized_path = sanitize_for_root(out_path)
    with open(out_sanitized_path, 'w') as f:
        f.writelines(functions)

    logger.info(f'Functions written to {out_path}')
    logger.info(f'Please add `from {out_path.replace("/", ".").replace(".py", "")} from *` to {in_path} to use these functions')

def test(func_name, cache_path="gen/gen.json"):
    data = get_json_from_file(cache_path)


if __name__ == "__main__":
    fire.Fire(generate)




