# metrika_runner
Library to run and measure benchmarks with scientific rigor.

To see an example of how to use it, look at metrika_benchs_game. Basically, the only
thing needed is to call `metrika_runner.start` with a list of benchmarks and a meter
object. 

Different studies require different measures and have different ways of executing
the benchmarks. For this reason, the library provides a layer to abstract common patterns,
and leaves the user the responsibility to implement benchmark specific stuff. The
main objective is to allow obtaining statistically solid measures. In order to do
that, the library executes the benchmarks many times and (should) present results
that take into account things like expected value (esperanza), standard deviation,
etc. 

To run a benchmark, the library asks for a user-written object implementing
metrika_executor interface. The only need is to implement `run_using(self, timer)`.
This method will have to start measuring, run the benchmark and stop.
The benchmark's metric can be anything: total time, memory consumption, cpu utilization,
whatever. The base library implements some simple meters: an abstract counter and a timer.
The abstract counter accepts any measure given by the user, it is useful for things like
measuring processor clock cycles with the `RDTSC` x86 instruction. The timer performs
plain execution time measuring.
 
The results of the benchmark can finally be passed to the reporter, to show them in
console.

Some things be done that come to mind: 


- support for running only some variations of the bench by command line arguments
- setting processor affinity
- setting clock frequency to maintain it stable (I think best would be to under-clock it).
- a meter to measure memory consumption
- outputing in different formats,
- creating other projects to show results: export to pdf, svg, etc.
- support for showing progress of metrics throughout implementation lifetimes
