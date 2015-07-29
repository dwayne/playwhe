How do I update the database of results?

    $ python playwhe.py -u "<path to>/playwhe/data/playwhe.db"

How do I register it with PyPI?

    $ python setup.py register

How do I distribute it?

    $ python setup.py sdist upload

Useful docs:

- https://docs.python.org/2/distutils/packageindex.html

Things to do when recreating the database of results from scratch:

1. Fix the [invalid draw number issue](https://bitbucket.org/dwaynecrooks/playwhe-restapi/issues/2/invalid-draw-number-in-data).

  ```
  $ sqlite3 playwhe.db
  > UPDATE results SET draw = 12168 WHERE draw = 16168;
  ```
