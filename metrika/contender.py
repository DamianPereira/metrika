
class Contender:
    def __init__(self, names, values):
        self.names = names
        self.values = values

    def __repr__(self):
        strings = tuple(str(v.id()) for v in self.values)
        return str(strings) + " contender"

    def __getitem__(self, item):
        idx = self.index_of(item)
        return self.values[idx]

    def index_of(self, varname):
        return self.names.index(varname)

    def id(self):
        return tuple(v.id() for v in self.values)

    def set_executor(self, executor):
        self.executor = executor

    def run(self, options, invocation):

        return self.executor.run_with(options, invocation)



