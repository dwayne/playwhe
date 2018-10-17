#!/usr/bin/env bash
#
# Usage: ./bin/results.sh
#
# Write the contents of playwhe.db as CSV to the data/results.csv file.

sqlite3 -noheader -csv playwhe.db 'select draw,date,period,number from results' > data/results.csv
