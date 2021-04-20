# Development guide
Get the repository

    git clone https://github.com/siforrer/coreali

Install dependencies

    pip install mkdocs
    pip install systemrdl-compiler
    pip install invoke

Some useful commands can be started with invoke. For example run the unit tests

    python -m invoke test

or just make all (test, documentation, package):

    python -m invoke all

and then install the locally created package in your python distribution

    python -m invoke install



