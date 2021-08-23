# Development guide
Get the repository

    git clone https://github.com/siforrer/coreali

Install dependencies

    python -m pip install -r tests/requirements.txt

Some useful commands can be started with invoke. For example run the unit tests

    python -m invoke test

or just make all (test, documentation, package):

    python -m invoke all

and then install the locally created package in your python distribution

    python -m invoke install

Or show this documentation:

	python -m mkdocs serve


