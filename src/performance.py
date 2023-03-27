import pandas as pd
import signal
import time

from simple_syntax_repair import *

# GLOBAL PARAMETERS BEGIN
total_time_elapsed = 0


# GLOBAL PARAMETERS END


def run_integration_test(input_path, output_path):
    """Integration testing, if interrupted in the middle, can continue next time."""

    def handle_keyboard_interrupt(signal, frame):
        """Define signal handling functions to handle keyboard interrupts."""
        global total_time_elapsed
        log_info("Keyboard interrupted, results being saved", "red")
        log_info("Current accuracy: {round(result['isFixed'].mean(), 3)}", "blue")
        total_time_elapsed += time.time() - start_time
        index = result.index[-1] + 1
        result.loc[index, 'id'] = total_time_elapsed
        result.to_csv(output_path, index=False)
        exit(0)

    assert os.path.dirname(input_path) == os.path.dirname(output_path), "Input and output must be in the same directory"
    filepath = os.path.dirname(input_path) + "/"

    # Set the signal processing function
    signal.signal(signal.SIGINT, handle_keyboard_interrupt)
    columns = ['id', 'sourceText', 'targetText', 'fixedText', 'isFixed', 'status']

    # Read the line number of the last interrupt (if any)
    try:
        result = pd.read_csv(output_path)
        start_line_number = result.index[-1]
        total_time_elapsed = result.loc[start_line_number, 'id']
        log_info(f"Starting from line  {start_line_number}", "yellow")
        log_info(f"Current accuracy: {round(result['isFixed'].mean(), 3)}", "yellow")
    except FileNotFoundError:
        start_line_number, total_time_elapsed = 0, 0.0
        # Create an empty output CSV file
        log_info(f"Creating new output file {output_path}", "yellow")
        result = pd.DataFrame(columns=columns)
        result.to_csv(output_path, index=False)

    df = pd.read_csv(input_path)
    start_time = time.time()

    for i in range(start_line_number, len(df)):
        row = df.iloc[i]
        sourceText = row['sourceText']

        try:
            prompt = generate_prompt(sourceText, filetype='c', isText=True)
            fixedText, isFixed = iterate_to_find_solution(prompt, sourceText, filepath=filepath, filetype='c',
                                                          isText=True)
            status = 'PASS' if isFixed else 'FAIL'
            log_info(f"Line {i}: {status}", "green" if isFixed else "red")
        except Exception as e:
            isFixed, status, fixedText = False, 'ERROR', 'Error generating output'
            log_info(str(e), 'red')

        # save to the result dataframe
        result.loc[i] = [row['id'], sourceText, row['targetText'], fixedText, isFixed, status]

    total_time_elapsed = time.time() - start_time
    log_info(f"Total time elapsed:', {total_time_elapsed}, seconds", "green")
    result.to_csv(output_path)
    log_info(f"Syntax repair accuracy: {round(result['isFixed'].mean(), 3)}", "green")


# Temporarily used to view un-fixed programs
def fewShotGlance(input_path, output_path):
    df = pd.read_csv(input_path)
    result = pd.read_csv(output_path)
    for i in range(len(result)):
        row = result.iloc[i]
        if not row['isFixed']:
            print("Line", i, "is not fixed")
            sourceText, targetText, fixedText = row[['sourceText', 'targetText', 'fixedText']]
            log_info(sourceText, "red")
            log_info(targetText, "green")
            log_info(fixedText, "blue")
            prutor, clangParse = df.loc[i, ['sourceErrorPrutor', 'sourceErrorClangParse']]
            log_info(prutor, "red")
            log_info(clangParse, "red")
            prompt = generate_prompt(sourceText, filetype='c', isText=True, errorInfo=[prutor, clangParse])
            log_info(prompt, "yellow")
            program, isFixed = iterate_to_find_solution(prompt, sourceText, filepath="../data/cdata/", filetype='c',
                                                        isText=True)
            log_info(program, "green") if isFixed else log_info(program, "red")
