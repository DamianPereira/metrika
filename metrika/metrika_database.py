
import os.path
import yaml


class MetrikaDatabase:
    def __init__(self, testbed):
        self.testbed = testbed
        self.filename = 'results-' + testbed + '.yml'
        self.results = self.load()

    def load(self):
        if not os.path.isfile(self.filename):
            return {}
        with open(self.filename, 'r+') as f:
            return yaml.load(f)

    def save(self, new_results):
        for executor, measures in new_results.items():
            self.results[executor.identity()] = measures

        with open(self.filename, 'w') as out:
            stream = '{\n'
            for (id, measures) in sorted(self.results.items()):
                stream += '    "%s": ' % id
                stream += str(measures) + ',\n'

            stream = stream[:-2]
            stream += '\n}'
            #stream = yaml.dump(self.results, default_flow_style=False)
            return out.write(stream)

    def reject_already_measured_in(self, executors):
        new_plan = []
        for executor in executors:
            if executor.identity() not in self.results.keys():
                new_plan.append(executor)

        return new_plan

    def measured_results_of(self, executors):
        results = {}
        for executor in executors:
            if executor.identity() not in self.results:
                print("Measure missing for " + executor.identity())
                continue

            results[executor] = self.results[executor.identity()]

        return results

