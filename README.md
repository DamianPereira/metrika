# Metrika
Metrika is a library to run and measure benchmarks with scientific rigor.
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
For quick examples of how to use Metrika, look at `metrika_benchs_simple`, `metrika_benchs_cooperative` or `metrika_benchs_game`.

The center of the library is the MetrikaEngine.
It knows to handle command line arguments and to
issue high-level actions like running benchs, reporting
results and plotting.
Users should create an instance of this class and pass
to it an outliner object, which handles particular user
needs.
The engine is generic, and the outliner has to be
written by the users to meet their specific needs.
The outliner creates instances of Benchmarks and
Contenders, and combines them through Executors.
Instances of Executor are in charge of running
benchmarks with specific contenders.
Usually users have to subclass MetrikaExecutor to
accommodate to their needs.
The executors also have to do measuring themselves,
or at least gather the results left by the contenders
after they are run.

Benchmark metrics can be anything: total time, memory consumption, cpu utilization, whatever.
The base library implements some simple meters: an abstract counter and a timer.
The abstract counter accepts any measure given by the user, it is useful for things like
measuring processor clock cycles with the `RDTSC` x86 instruction. The timer performs
plain execution time measuring.

The results of the benchmark can finally be passed to the reporter, to show them in
console.

Some things to be done that come to my mind:


- improve command line argument handling
- setting processor affinity
- setting clock frequency to maintain it stable (I think best would be to under-clock it).
- a meter to measure memory consumption
- outputting in different formats,
- creating other projects/modules to show results: export to pdf, svg, etc.
- support for showing progress of metrics throughout implementation lifetimes
