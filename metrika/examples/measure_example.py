# measure_example.py

from metrika.suite import Suite

programs = {
    'str': "'-'.join(str(n) for n in range(%d))",
    'list': "'-'.join([str(n) for n in range(%d)])"
}

sizes = {'test': 10, 'small': 10000, 'big': 1000000}


def configure(engine):
    suite = Suite()
    suite.add_variable_from_dict('program', programs)
    suite.add_variable_from_dict('size', sizes)

    setup = engine.organize_experiment(suite, 'join-perf')
    setup.invoke_with_command(lambda program, size: 'python -c "%s"' % (program % size))
    setup.measure_execution_time()
