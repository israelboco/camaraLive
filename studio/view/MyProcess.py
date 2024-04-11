import multiprocessing


class MyProcess():
    def __init__(self, target_function, args=()):
        super().__init__()
        self.target = target_function
        self.args = args

    def run(self):
        process = multiprocessing.Process(target=self.target, args=self.args)
        process.start()
        process.join()
        