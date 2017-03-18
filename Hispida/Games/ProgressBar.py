import sys

class ProgressBar():

    def __init__(self):
        self.total = 42
        sys.stdout.write("[" + " "*self.total + "]")
        sys.stdout.flush()
        sys.stdout.write("\b"*(self.total+2) + "[")

    def next(self):
        sys.stdout.write("#")
        sys.stdout.flush()
        self.total -= 1

    def end(self):
        sys.stdout.write("#" * self.total + "]\n")
        sys.stdout.flush()

