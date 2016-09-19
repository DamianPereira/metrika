# Metrika
Metrika is a library to run benchmarks and measure results with scientific rigor.
By automating the process of benchmark running, scientists can avoid
common mistakes.
Metrika allows to obtain statistically solid measures without accidentally introducing methodological
errors. In order to do
that, the library executes the benchmarks many times and presents results
taking into account things like expected value (esperanza), standard deviation,
etc.

 Metrika tries to reduce two main sources of errors:

- **Methodological errors**:
Manually running benchmarks can lead to subtle slips like mixing bench
results of different testbeds, or with different power settings,
input values, etc.
Metrika provides ways of setting up variations of benchmarks with different
inputs and execution flags, and executes them with minimal human intervention.
Using meters provided by the library prevents mistakes when measuring.


- **Data analysis errors**: Results of benchmarks should be preserved
for future examination when needed.
Metrika stores on a database in disk the measures
obtained, and can reload them for
further inspection later. The library provides tools for assessing
the quality of results: averages, standard deviation, confidence
intervals and outliers are automatically calculated and shown.


Motivation
-----

Different studies require different measures and have different ways of executing the benchmarks.
Sometimes the need is to just measure one implementation  (`contender` in metrika parlance) run-time against another.
Other times it is require to vary the inputs, or to measure
things like memory usage.
Other need can be to only measure the program during some interval (like after warm-up).
In that case the program has to perform the measuring itself
and pass it back to the framework.
As can be seen, the number of options is large. For this reason, the library provides a layer to abstract common patterns,
and leaves to the user the responsibility to implement specific stuff.

Usage
-----
For quick examples of how to use Metrika, look at `metrika_benchs_simple` or `metrika_benchs_game`.

The center of the library is the Engine.
It knows to handle command line arguments and to
issue high-level actions like running benchs, reporting
results and plotting.
Importing the module with

    $> python -m metrika
    
will create an engine, and search for experiment configurations in the 
current directory. An experiment is a file named `measure_*.py` that 
configures all things that need to be done; it is written by the user
of the library.
The engine will import each experiment and call its
corresponding `configure` method.
The configuration has to be written by the users to meet
their specific needs. The first thing it will need is a `Suite`,
which is a representation of the set of things that can vary in 
the experiment, such as input variables, program to execute, etc.
With the variables, the suite is used calculate all the combinations
of values that need to measured in the experiment.
Each combination instance is called a contender. 
An `Experiment` combines a suite, an executor and a meter to obtain
results. To do that, it creates the contenders and executes them
measuring with the meter that has been set.

An example of a very simple configuration is this:

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

This measures time elapsed to join lists of strings using different
implementations. It can be run with:

    $> python -m metrika run -i 28 -x join-perf -r size=big

    experiments to run: {join-perf exp: [('str', 'big') contender, ('list', 'big') contender]}
    experiments skipped: [join-perf exp]

    Running experiment join-perf
    running 28 passes of ('str', 'big') contender. 
    1... 2... 3... 4... 5... 6... 7... 8... 9... 10... 11... 12... 13... 14... 15... 16... 17... 18... 19... 20... 21... 22... 23... 24... 25... 26... 27... 28... 
    running 28 passes of ('list', 'big') contender. 
    1... 2... 3... 4... 5... 6... 7... 8... 9... 10... 11... 12... 13... 14... 15... 16... 17... 18... 19... 20... 21... 22... 23... 24... 25... 26... 27... 28... 
    -----
    join-perf time
    -----
    contender |     input      | median | std dev % | runs 
    ==========+================+========+===========+=====
          str |    big:1000000 |  0.396 |    3.47 % |   28 
         list |    big:1000000 |  0.426 |    2.47 % |   28 
    ......... | .............. | ...... | ......... | .... 
    
    results obtained at 2016-09-19 16:43:13.002494 in the following system:

    testbed: example-laptop
    os:  Ubuntu 16.04 xenial (Linux-4.4.9-040409-generic-x86_64).
    cpu: Intel(R) Core(TM) i7-4510U CPU @ 2.00GHz (@2.85 GHz), 4096 KB l2 cache, 4 logical cores (2 physical)
    mem: 7912 MB phys, 145 MB free

Benchmark metrics can be anything: total time, memory consumption,
cpu utilization, whatever.
The base library implements some simple meters: an abstract counter,
a timer, and a file reader.
 - The `Meter` is an abstract counter that accepts any measure given
  by the user. It can be useful for things like measuring processor
  clock cycles with the `RDTSC` x86 instruction.
 - The `Timer` performs execution time measuring with a Python timer.
 - The `FileMeter` parses a result file to obtain results. In this
   case, the execution of the contender should generate an output
   file to be read.

The results of the experiment can finally be passed to the reporter,
to show them in console, and to the plotter to generate a pdf figure.
Those are very basic and generic, improvements are welcome.

Some things to be done that come to my mind:

- think if refactoring framework to use panda lib instead of
  hand made variables, values, etc would be an improvement
- save more info about the experiments run (depends on previous item?)
- improve command line argument handling
- better handling of errors (specially when called with bad arguments)
- implement setting processor affinity
- implement setting clock frequency to maintain it stable (I think best
 would be to under-clock it, disabling turbo at least).
- better handle results with multiple measures
- generate output in different formats,
- make plotting optional (to be able to run without matplotlib)
- export to svg or other formats etc.
- better showing progress of experiments
- allow to test that measured things are being executed correctly 
- showing metrics progression throughout VCS lifetimes (ie. git commits)
