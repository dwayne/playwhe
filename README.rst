playwhe
=======

A Python library and CLI for fetching and storing Play Whe results from the
`National Lotteries Control Board <http://www.nlcb.co.tt/>`_ (NLCB).

I originally wrote :code:`playwhe` in 2011 when I wanted to work on a small
project to build a RESTful API for Play Whe. The project has grown since then
and this code continues to play a key role in it.

:code:`playwhe` helps many people to conveniently access Play Whe results.

Installation
------------

To install, simply use pip (or `pipenv`_):

.. code-block:: bash

    $ pip install playwhe

.. _pipenv: https://github.com/pypa/pipenv

Usage
-----

The library supports the implementation of the CLI. In the future, a developer
would also be able to use the library within another application to query a
database of Play Whe results in useful and interesting ways.

**So what can the CLI do?**

There are 3 main things you can do with :code:`playwhe` on the command-line:

1. Initialize a database for storing Play Whe results.
2. Load existing Play Whe results from a CSV file into the database.
3. Update the database with the latest results from NLCB's servers.

**Initialize**

To initialize a database for storing Play Whe results you need to run the
following:

.. code-block:: bash

    $ playwhe --verbose --init sqlite:///$HOME/playwhe.db

The command creates a new SQLite database in the :code:`playwhe.db` file in the
:code:`$HOME` directory. The database contains the tables needed for storing the
Play Whe results.

Once the database has been initialized you can begin to load or update the Play
Whe results as needed.

**Load**

To load Play Whe results from a CSV file into the database you need to run the
following:

.. code-block:: bash

    $ playwhe --verbose --load data/results.csv sqlite:///$HOME/playwhe.db

:code:`results.csv` is a CSV file that contains the results you intend to load
into the database.

Each line in the CSV file needs to be in the format:

.. code-block::

    <draw:1|2|3|...>,<date:yyyy-mm-dd>,<period:EM|AM|AN|PM>,<number:1-36>

The load command is intended to be used, only once, when you're starting off
with an empty database, i.e. when you've just initialized the database. In fact,
you can initialize and load the database in one command by running the
following:

.. code-block:: bash

    $ playwhe -Vil data/results.csv sqlite:///$HOME/playwhe.db

:code:`-V` is shorthand for :code:`--verbose`, :code:`-i` is shorthand for
:code:`--init` and :code:`-l` is shorthand for :code:`--load`.

You can find a necessarily out-of-date :code:`results.csv` file in the
:code:`data` directory of this project. I update it occasionally so that you
don't have to do too much updating when you're starting from an empty database.

Another benefit of using :code:`data/results.csv` is that if there's any error
in the results provided by NLCB then I usually fix it in the CSV file. So at
least you know you're starting off with good data.

**Update**

To update the database with the latest results from NLCB's servers you need to
run the following:

.. code-block:: bash

    $ playwhe --verbose --update sqlite:///$HOME/playwhe.db

If you're starting from an empty database or a really out-of-date database then
be prepared to wait a while since the program has to fetch the data from a
remote server.

The :code:`--verbose` option is not necessary but it's helpful. Use it to keep
track of the task when you're running it interactively.

If you intend to update using a cron job then I'd recommend removing the
:code:`verbose` flag and also redirecting standard error to a log file. Here's
what the command would look like:

.. code-block:: bash

    $ playwhe --update sqlite:///$HOME/playwhe.db 2>> $HOME/playwhe.log

**What else can the CLI do?**

Not much else at the moment but you can always access help to get a refresher
on how to perform a certain task:

.. code-block:: bash

    $ playwhe --help

Development
-----------

Recommended tools:

 - `pyenv <https://github.com/pyenv/pyenv>`_
 - `pipenv`_

Clone the repository and install the dependencies:

.. code-block:: bash

    $ git clone git@github.com:playwhesmarter/playwhe.git
    $ cd playwhe
    $ pipenv shell
    $ pipenv install --dev

You're now all set to begin development.

Testing
-------

Tests are written using the built-in unit testing framework, `unittest <https://docs.python.org/3/library/unittest.html>`_.

Run all tests.

.. code-block:: bash

    $ python -m unittest

Run a specific test module.

.. code-block:: bash

    $ python -m unittest tests.playwhe.client.test_fetcher

Run a specific test case.

.. code-block:: bash

    $ python -m unittest tests.playwhe.client.test_fetcher.FetchFromMockServerTestCase.test_when_it_succeeds

Run a test against the real server.

.. code-block:: bash

    $ PLAYWHE_TESTS_USE_REAL_SERVER=1 python -m unittest tests.playwhe.client.test_fetcher.FetchFromRealServerTestCase

Resources
---------

- `NLCB <http://www.nlcb.co.tt/>`_
