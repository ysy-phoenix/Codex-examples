import requests
import json

# GLOBAL PARAMETERS BEGIN
MAX_TOKENS = 1000
url = "https://eviloder.win/v1/completions"  # my personal domain
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + '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'
}

# GLOBAL PARAMETERS END

def generate_prompt(practice_description, target_language, compiler_info, user_code):
    prompt = '# Fix errors in the below file written in, and point out the error line in comments. Your comment should on a new line before the error line.\n'
    prompt += '# The program is to solve the following problem.\n'
    prompt += '\n[[To be solved Problem]]\n' \
            '### To be solved Problem ###\n'
    prompt += practice_description + '\n'

    prompt += '# The file is written in ' + target_language + '.\n'
    prompt += '# The compiler information is ' + compiler_info + '.\n'
    prompt += '\n[[Buggy Program]]\n' \
              '### Buggy Program ###\n'
    prompt += user_code + '\n'

    prompt += '\n[[Fixed Program]]\n' \
              '### Fixed Program ###\n'
    return prompt


def generate_completion(input_prompt, num_tokens=MAX_TOKENS, temperature=0.5):
    data = {
            "model": "text-davinci-003",
            "prompt": input_prompt,
            "temperature": temperature,
            "max_tokens": num_tokens,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "stop": ["###"]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


def find_solution(practice_description, target_language, compiler_info, user_code):
    input_prompt = generate_prompt(practice_description, target_language, compiler_info, user_code)
    response = generate_completion(input_prompt, num_tokens=MAX_TOKENS)
    return response['choices'][0]['text']
