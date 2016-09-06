# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = "metrika",
    packages = ["metrika"],
    version = "0.0.1",
    description = "Benchmark framework for scientists",
    author = "Javier Pimás",
    author_email = "elpochodelagente@gmail.com",
    url = "https://github.com/dc-uba/metrika",
    keywords = ["benchmark", "measure", "automatic", "rigorous"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Benchmark",
        "Topic :: Scientific/Engineering"
        ],
    long_description = """\
Benchmark framework for scientists
----------------------------------

Metrika is a library to run and measure benchmarks with
scientific rigor. By automating the process of benchmark
running, scientists can avoid common mistakes. Metrika
allows to gather statistically solid measures without
accidentally introducing methodological errors. In order
to do that, the library executes the benchmarks many times
and presents results taking into account things like expected
value, standard deviation, etc.

This version requires Python 3 or later
"""
)