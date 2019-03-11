# Notes

## How to get CSV results from the old version of the Play Whe database?

Firstly, get the latest Play Whe results from the old version of the database:

```sh
ssh dwaynecrooks:.playwhe/playwhe.db .
```

Then, export the results into CSV format:

```sh
sqlite3 -noheader -csv playwhe.db 'select draw,date,period,number from results' > data/results.csv
```
