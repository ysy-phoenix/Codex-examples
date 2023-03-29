import os

# GLOBAL PARAMETERS BEGIN
MAX_TOKENS = 1000
url = os.environ['OPENAI_API_URL']  # my personal domain
DEFAULT_MODEL = "text-davinci-003"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + os.environ['OPENAI_API_KEY']
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
LANGUAGE_TO_FILE_TYPE = {
    "python": "py",
    "c": "c",
    "c++": "cpp",
    "java": "java",
}


# GLOBAL PARAMETERS END


def log_info(msg, color):
    """Log info with different color."""
    print(COLOR_TO_ESCAPE[color], msg, "\033[0m", sep='')
