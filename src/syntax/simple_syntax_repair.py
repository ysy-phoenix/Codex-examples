import openai
import requests
import json

from src.base.utils import *
from src.syntax.syntax_oracle import *

# GLOBAL PARAMETERS BEGIN
DEBUG = True
ISURL = True
# url = "https://api.openai.com/v1/completions"
FILE_PATH = "../data/pydata/"


# GLOBAL PARAMETERS END


def initialize_openai_api():
    """Initialize the OpenAI API from OS environment variables."""
    openai.api_key = os.environ['OPENAI_API_KEY']
    if not openai.api_key:
        log_info("Please set the OPENAI_API_KEY environment variable!", "red")
        sys.exit(1)


def generate_syntax_prompt(practice_description, target_language, compiler_info, user_code, errorInfo=None):
    """
    Generate prompt for Codex.
    Now only with buggy program, error info is optional.
    """
    if errorInfo is None:
        errorInfo = []

    prompt = '# Fix syntax errors in the below program.\n'
    prompt += '# Please point out the error line in comments.\n'
    prompt += '# Also point out how you fixed it.\n'

    if practice_description != '':
        prompt += '# The program is to solve the following problem.\n'
        prompt += '\n[[Problem Description]]\n' \
                  '### Problem Description ###\n'
        prompt += practice_description + '\n'

    prompt += '# The code is written in ' + target_language + '.\n'

    if compiler_info != '':
        prompt += '# The compiler information is ' + compiler_info + '.\n'

    prompt += '# Some error information will also be provided.\n' if errorInfo != [] else ''
    for i, e in enumerate(errorInfo):
        prompt += f"\n[[Error Info {i + 1}]]\n"
        prompt += f"### Error Info {i + 1} ###\n"
        prompt += e + '\n'

    prompt += '\n[[Buggy Program]]\n' \
              '### Buggy Program ###\n'
    prompt += user_code + '\n'

    prompt += '\n[[Fixed Program]]\n' \
              '### Fixed Program ###\n'

    return prompt


def generate_completion(input_prompt, num_tokens=MAX_TOKENS, temperature=0.8):
    """Generate completion for Codex."""
    log_info("Waiting for Codex response ...\n", "green") if DEBUG else None
    if ISURL:
        data = {
            "model": DEFAULT_MODEL,
            "prompt": input_prompt,
            "temperature": temperature,
            "max_tokens": num_tokens,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "stop": ["###"]
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            log_info(f"Error: {response.status_code}", "red")
            return None
    else:
        try:
            response = openai.Completion.create(
                model=DEFAULT_MODEL,
                prompt=input_prompt,
                temperature=temperature,
                max_tokens=num_tokens,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=["###"]
            )
            return response
        except Exception as e:
            log_info(f"Error: {e}", "red")
            return None


def write_to_file(file, filepath, program):
    """Save the fixed program to a file."""
    with open(filepath + file, "w") as f:
        f.write(program)


def iterate_to_find_solution(practice_description, target_language, compiler_info, user_code, filepath, errInfo=None,
                             max_time=3):
    """Iterate several times to find a solution."""
    if errInfo is None:
        errInfo = []
    fixed_file = "fixed." + LANGUAGE_TO_FILE_TYPE[target_language]
    filepath += "tests/"
    program = ""
    syntax_oracle = LANGUAGE_TO_ORACLE[target_language](fixed_file, filepath)
    input_prompt = generate_syntax_prompt(practice_description, target_language, compiler_info, user_code, errInfo)

    log_info("Codex is looking for a solution ...", "blue") if DEBUG else None
    for _ in range(max_time):
        response = generate_completion(input_prompt, num_tokens=MAX_TOKENS)
        program = response['choices'][0]['text']
        write_to_file(fixed_file, filepath, program)
        if syntax_oracle.test() == 'OK':
            log_info(program, "cyan") if DEBUG else None
            return program, True

    log_info("Codex can not find a solution!", "magenta") if DEBUG else None
    return program, False
