import os
import openai

from syntax_oracle import *

DEBUG = True
MAX_TOKENS = 1000
FILE_PATH = "../data/pydata/"
FILE_TYPE_TO_LANGUAGE = {
    "py": "python",
    "c": "c",
    "cpp": "c++",
    "java": "java",
}
COLOR_TO_ESCAPE = {
    "red": "\033[31;1m",
    "green": "\033[32;1m",
    "yellow": "\033[33;1m",
    "blue": "\033[34;1m",
    "magenta": "\033[35;1m",
    "cyan": "\033[36;1m",
    "white": "\033[37;1m",
}
FILE_TYPE_TO_ORACLE = {
    "py": PySyntaxOracle,
    "c": CSyntaxOracle,
    "cpp": CppSyntaxOracle,
}


def log_info(msg, color):
    """
    Log info with different color.
    """
    print(COLOR_TO_ESCAPE[color] + msg + "\033[0m")


def initialize_openai_api():
    """
    Initialize the OpenAI API from OS environment variables.
    """
    openai.api_key = os.environ['OPENAI_API_KEY']
    if not openai.api_key:
        print("Please set the OPENAI_API_KEY environment variable.")
        sys.exit(1)


def generate_prompt(source, filepath=None, filetype=None, isText=False):
    """
    Generate prompt for Codex.
    Now only with buggy program.
    """
    resPrompt = '\n===================================================\n' \
                '# Fix syntax error in the below file written in '
    if not isText:
        filetype = source.split(".")[1]
    resPrompt += FILE_TYPE_TO_LANGUAGE[filetype] + '.\n'
    resPrompt += '\n[[Buggy Program]]\n' \
                 '### Buggy Program ###\n'
    if isText:
        resPrompt += source + '\n'
    else:
        with open(filepath + source) as f:
            resPrompt += f.read() + '\n'

    resPrompt += '\n[[Fixed Program]]\n' \
                 '### Fixed Program ###\n'
    return resPrompt


def generate_completion(input_prompt, num_tokens=MAX_TOKENS, temperature=0.8):
    """
    Generate completion for Codex.
    """
    log_info("Waiting for Codex response ...\n", "green") if DEBUG else None
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=input_prompt,
        temperature=temperature,
        max_tokens=num_tokens,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["###"]
    )
    return response


def write_to_file(file, filepath, program):
    """
    Save the fixed program to a file.
    """
    with open(filepath + file, "w") as f:
        f.write(program)


def iterate_to_find_solution(input_prompt, file, filepath=None, filetype=None, isText=False, max_time=3):
    """
    Iterate several times to find a solution.
    """
    if not isText:
        filename, filetype = file.split(".")
    else:
        filename = "temp"
    fixed_file = filename + "_fixed." + filetype
    filepath += "tests/"
    syntax_oracle = FILE_TYPE_TO_ORACLE[filetype](fixed_file, filepath)

    log_info("Codex is looking for a solution ...", "blue") if DEBUG else None
    for _ in range(max_time):
        response = generate_completion(input_prompt, num_tokens=MAX_TOKENS)
        program = response['choices'][0]['text']
        write_to_file(fixed_file, filepath, program)
        if syntax_oracle.test() == 'OK':
            log_info(program, "cyan") if DEBUG else None
            return program

    log_info("Codex can not find a solution!", "magenta") if DEBUG else None
    return None



