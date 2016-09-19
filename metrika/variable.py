
class Variable:
    def __init__(self, name, values):
        self.name = name
        self.values = values

    def __repr__(self):
        return "var " + self.name + "(" + ','.join([str(v.id()) for v in self.values]) + ")"

    def restrict_to(self, value):
        self.values = [next((val for val in self.values if val.is_named(value)), value)]


class AnonValue:
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return ":" + str(self._value)

    def __lt__(self, other):
        return self._value < other._value

    def id(self):
        return self._value

    def is_named(self, name):
        return False

    def value(self):
        return self._value


class NamedValue:
    def __init__(self, name, value):
        self.name = name
        self._value = value

    def __repr__(self):
        return self.name + ":" + str(self._value)

    def __lt__(self, other):
        return self._value < other._value

    def id(self):
        return self.name

    def is_named(self, name):
        return self.name == name

    def value(self):
        return self._value

