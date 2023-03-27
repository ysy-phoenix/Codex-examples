import subprocess
import sys


class SyntaxOracle:
    """Simple Syntax Oracle."""

    def __init__(self, file, filepath):
        self.file = file
        self.filepath = filepath
        self.src = filepath + file
        self.bin = filepath + file.split(".")[0] + ".exe"
        self.args = None

    def test(self, timeout=3):
        try:
            p = subprocess.run(
                self.args,
                stdout=sys.stdout,
                stdin=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                timeout=timeout
            )
        except subprocess.TimeoutExpired:
            return 'TIMEOUT'

        if p.returncode != 0:
            return 'ERROR'

        return 'OK'


class CSyntaxOracle(SyntaxOracle):
    def __init__(self, file, filepath):
        super().__init__(file, filepath)
        self.args = ["gcc", "-w", "-O2", self.src, "-o", self.bin]


class CppSyntaxOracle(SyntaxOracle):
    def __init__(self, file, filepath):
        super().__init__(file, filepath)
        self.args = ["g++", "-w", "-O2", self.src, "-o", self.bin]


class PySyntaxOracle(SyntaxOracle):
    def __init__(self, file, filepath):
        super().__init__(file, filepath)
        self.args = ["python", self.src]
