import pandas

from src.performance import *
from src.base.code_fix_api import *


def simple_test():
    testfile = "../data/cdata/singleL_Test.csv"
    data = pandas.read_csv(testfile)
    initialize_openai_api()
    for i in range(3):
        row = data.iloc[i]
        source = row['sourceText']
        program = find_solution("", 'cpp', "", source)
        log_info(program, "green")


if __name__ == "__main__":
    simple_test()
    # input_path, output_path = "../data/cdata/singleL_Test.csv", "../data/cdata/singleL_Test_result.csv"
    # run_integration_test(input_path, output_path)
    # fewShotGlance(input_path, output_path)
    # program 52 is fixed successfully with error information provided! 2023.03.27 20:15:00
