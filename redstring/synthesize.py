import openai
import ast
import re
import json
from decouple import config
from datetime import datetime
from deprecated import deprecated
from loguru import logger
from astlib.base import PrgAST
from redstring.parser import get_undefined_functions
from utils import sanitize_for_root, dump_json_to_file

openai.api_key = config('KEY')

class InputArg:
    def __init__(self, name, argtype= None):
        self.name = name
        self.argtype = None

    def __repr__(self):
        if self.argtype:
            return f'{self.name} of {self.argtype}'
        else:
            return f'{self.name}'

class DesiredFunction:
    def __init__(self, func_name, inputs):
        self.func_name = func_name
        self.inputs = inputs
        self.num_inputs = len(inputs)
        self.num_outputs = 1

def get_prompt_prologue() -> str:
    """
    For prompt engineering, we give the synthesizer a pattern to match, to reduce noise.
    :return: A string that will precede the prompt query to the synthesizer.
    """

    return '''You are a programmer that is excellent at writing Python code. Given previously defined functions, you create a new one. Do not assume any non-given functions. 

An example:
Given functions:
def sanitize(text):
    text = text.replace("\s", "\q")
    return text

Task: Create a function read_file that accepts 1 input. It returns 1 output.
Code:
def read_file(filename):
    file = open(x0, 'r');
    text = file.read()
    text = sanitize(text)
    file.close()
    return text

END
'''

@deprecated(version="0.1.0", reason="typing from I/O TBD")
def get_io_types_string(func_args) -> str:
    """
    :param func_args: The input/output values from a node.
    :return: A string conjoining all the types of input output values to help the prompt to the synthesizer.
    """
    return ' and '.join([arg.var_type for arg in func_args])


def get_arg_list(node) -> str:
    """
    :param inputs: The input values from a node
    :return: A function signature arguments for the number of input values to the node.
    """
    return ', '.join([inp.name for inp in node.inputs])

def get_prompt(node, prev_gens, prg) -> str:
    collected_prev_functions = "\n".join(prev_gens)
    if prg:
        collected_prev_functions = prg.prg_str + "\n" + collected_prev_functions

    return f'''
Given functions:
{collected_prev_functions}
Task: Create a function {node.func_name} that accepts {node.num_inputs} inputs. It returns {node.num_outputs} outputs.
Code:
def {node.func_name}({get_arg_list(node)}):'''

def format_generated_code(node, generated_code) -> str:
    return f'def {node.func_name}({get_arg_list(node)}):{generated_code}'

def generate_code_for_node(node, prev_gens=[], prg=None) -> str:
    """
    Given a node in a network, return the code that would perhaps the operation dictated by this node.
    :param node: The function node for which we are going to generate Python code.
    :return: A string representation of the python code generated.
    """
    prologue = get_prompt_prologue()
    prompt = prologue + get_prompt(node, prev_gens, prg)
    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        n=1,
        temperature=0,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["END"]
    )
    # TODO: Evaluate all options before returning value
    generated_code = response.choices[0]['text']
    formatted_code = format_generated_code(node, generated_code)
    logger.info(f"Defining function:\n{formatted_code}")
    return formatted_code

@deprecated(version="0.1.0", reason="with improved prompt engineering, don't need post-processing")
def gen_post_process(generated_code):
    return re.sub(r'\s{4}', '\t', generated_code.rstrip()) + "\n\n"

def get_function_from_metadata(func_name, func_args, prev_gens, prg):
    inputs = []
    random_var_count = 0
    for arg in func_args:
        if isinstance(arg, ast.Constant):
            inputs.append(InputArg(f'x{random_var_count}'))
            random_var_count += 1
        elif isinstance(arg, ast.Name):
            inputs.append(InputArg(arg.id))

    func_node = DesiredFunction(func_name, inputs)
    return generate_code_for_node(func_node, prev_gens, prg)

def cache_generation(cacher, path="gen/gen.json"):
    dump_json_to_file(cacher, path)

def get_generated_functions(prg):
    logger.add(f'gen/logs/{datetime.now().strftime("%y-%m-%d-%H-%M-%S")}.log')
    logger.info(f"Starting logging for {prg.prg_str}")

    undefined_calls = get_undefined_functions(prg)
    cacher = {}
    gen_func_strs = []
    for call in undefined_calls:
        func_name = call.func.id
        func_args = call.args
        # TODO: Integrate types in inputs
        # TODO: Integrate types for output when any
        function = get_function_from_metadata(func_name, func_args, gen_func_strs, prg)
        cacher[func_name] = function
        gen_func_strs.append(function)

    cache_generation(cacher)
    return gen_func_strs


if __name__ == '__main__':
    # prg = PrgAST.from_file("../tests/test_files/simple_generate.py")
    prg = PrgAST.from_file("../tests/test_files/multi_generate.py")
    funcs = get_generated_functions(prg)
    for func in funcs:
        logger.info(f"Defining function:\n{func}")
    with open("../gen/gen.py", "w") as f:
        f.writelines(funcs)



