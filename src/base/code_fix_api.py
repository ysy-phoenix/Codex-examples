import requests
import json

from base.utils import *


def generate_prompt(practice_description, target_language, compiler_info, user_code):
    """
    Generates a prompt for the OpenAI API.
    TODO: Pass more information to the prompt.
    """
    prompt = '# Fix errors in the below program.\n'
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

    prompt += '\n[[Buggy Program]]\n' \
              '### Buggy Program ###\n'
    prompt += user_code + '\n'

    prompt += '\n[[Fixed Program]]\n' \
              '### Fixed Program ###\n'
    return prompt


def generate_completion(input_prompt, num_tokens=MAX_TOKENS, temperature=0.5):
    """
    Generate code completion via OpenAI API.
    TODO: Find best parameters of the API.
    """
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
        return response.json()
    else:
        log_info(f"Error: {response.status_code}", "red")
        return None


def find_solution(practice_description, target_language, compiler_info, user_code):
    """
    Find solution for the given user code.(Now call OpenAI API once only)
    TODO: Divided into syntactic and semantic stages.
    TODO: Iterate several times to find the optimal solution.
    """
    input_prompt = generate_prompt(practice_description, target_language, compiler_info, user_code)
    response = generate_completion(input_prompt, num_tokens=MAX_TOKENS)
    return response['choices'][0]['text']
