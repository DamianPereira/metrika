
class Benchmark:
    def __init__(self, name, settings):
        self.name = name
        self.settings = settings

    def identity(self):
        return self.name + ' ' + str(self.settings)

    def __lt__(self, other):
        return self.identity() < other.identity()

    def __repr__(self):
        return self.identity()
