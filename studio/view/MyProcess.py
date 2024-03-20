import multiprocessing


class MyProcess(multiprocessing.Process):
    def __init__(self, target_function, args=()):
        super().__init__()
        self.target_function = target_function
        self.args = args

    def run(self):
        self.target_function(*self.args)