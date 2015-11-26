How do I update the database of results?

    $ python playwhe.py -u "<path to>/playwhe/data/playwhe.db"

How do I register it with PyPI?

    $ python setup.py register

How do I distribute it?

    $ python setup.py sdist upload

Useful docs:

- https://docs.python.org/2/distutils/packageindex.html

Things to do when recreating the database of results from scratch:

1. Fix the [invalid draw number issues](https://github.com/dwayne/playwhe/issues?utf8=%E2%9C%93&q=+is%3Aissue+label%3Afix-data-manually+)

  ```
  $ sqlite3 playwhe.db
  > UPDATE results SET draw = 12168 WHERE draw = 16168;
  > UPDATE results SET draw = 14456 WHERE draw = 14556;
  ```
