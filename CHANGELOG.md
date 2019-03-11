# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.8.0-alpha.2 (2019-03-16)

A refactoring of the library to have it expose a more useful public API.

### Added

- The `playwhe.client` module
- The `playwhe.cli` module
- A notes file, `NOTES.md`
- An environment variable condition on tests that use the real server. The
  environment variable is called `PLAYWHE_TESTS_USE_REAL_SERVER`

### Removed

- The `playwhe.scraper` module
- The `playwhe.db` module
- The `bin/results.sh` script

### Changed

- The public API

## 0.8.0-alpha.1 (2018-10-20)

A complete rewrite.

### Added

- The `playwhe.scraper` module
- The `playwhe.db` module
- The `bin/results.sh` script for saving results from a Play Whe database to a
  CSV file
- An archive of Play Whe results that's stored in the `data/results.csv` CSV
  file
- Support for logging
- A suite of tests
- A license, MIT
- A changelog

### Changed

- The CLI

## 0.7.1 (2017-12-10)

I forgot to make some important updates to the results in the Play Whe database
after making the changes in 0.7.

## 0.7 (2016-04-01)

The NLCB website occasionally has incorrect results. More often than not the
draw numbers are the culprit. However, if we order the data by date, then by
period and then by draw number we can mitigate any ill effects this bad data
causes.

### Removed

- Backup databases since it wasn't necessary to keep them in this project

### Fixed

- How data is retrieved so that invalid draw numbers don't affect the
  correctness of the data being displayed

## 0.6 (2015-07-28)

On July 6th, 2015 the NLCB started drawing Play Whe 4 times per day. Due to this
the `playwhe.py` script was updated to scrape the new 4:00pm draw.

### Changed

- `playwhe.py` to scrape the new 4:00pm draw
- Period from a number, one of `1, 2, 3`, to a string, one of `EM, AM, AN, PM`

### Fixed

- Bad results data in the backup Play Whe database

## 0.5 (2015-03-29)

Around February 21st, 2015 the NLCB took down their website to redesign and
rebuild it. They changed the service URL along with the format of the HTML
results. Due to this, the parser had to be updated.

### Added

- A few notes

### Changed

- The parser to parse results based on the new syntax
- The service URL

### Fixed

- The name of the Play Whe results backup file
- The regular expression used to parse results so that it ignores case

## 0.4 (2011-12-11)

On November 21st, 2011 the NLCB started drawing Play Whe 3 times per day. Due to
this, the display format of the results on their website changed. Since this
program simply scrapes the HTML off their results page, the script was updated
to work with the new format.

### Added

- Play Whe results up to December 10th, 2011

### Changed

- The `playwhe.py` script to work with NLCB's new format

### Fixed

- The long description in `setup.py`

## 0.3 (2011-06-28)

### Added

- A database to store Play Whe results
- Play Whe results from July 4th, 1994 to June 28th, 2011

### Changed

- The README
- The short description in `setup.py`

## 0.2 (2011-06-25)

### Added

- A README
- A `Mark` class

### Changed

- `playwhe.py` so that it can be used as both a script and module
- Rename `Draw` to `Result`
- The documentation
- The error messages

### Fixed

- `name_of_mark` bug
- `self.__mark` bug

## 0.1 (2011-05-14)

Initial release
