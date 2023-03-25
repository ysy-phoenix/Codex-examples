import pandas
from difflib import ndiff

from simple_syntax_repair import *


def simple_text_test():
    testfile = "../data/cdata/singleL_Test.csv"
    data = pandas.read_csv(testfile)
    initialize_openai_api()
    for i in range(5):
        row = data.iloc[i]
        source = row['sourceText']
        prompt = generate_prompt(source, filetype='cpp', isText=True)
        log_info(prompt, "yellow")
        program = iterate_to_find_solution(prompt, source, filepath="../data/cdata/", filetype='cpp', isText=True)
        # if program is not None:
        #     target = row['targetText']
        #     print(target == program)


def simple_file_test():
    # file = "test.py"
    # filepath = "../data/pydata/"
    file = "test.cpp"
    filepath = "../data/cppdata/"
    initialize_openai_api()
    prompt = generate_prompt(file, filepath=filepath)
    log_info(prompt, "yellow")
    iterate_to_find_solution(prompt, file, filepath=filepath)


if __name__ == "__main__":
    # simple_text_test()
    simple_file_test()