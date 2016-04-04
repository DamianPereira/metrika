

class Contender:
    def __init__(self, name, settings, commander):
        self.name = name
        self.settings = settings
        self.commander = commander

    def command_to_execute(self, bench, options):
        return self.commander(bench, self.settings['command'], options)
        # argument = bench.name + " " + str(bench.input)
        # return self.command + " " + argument

    def __repr__(self):
        return self.name
