# roastcalc

## ABOUT:
scrape.py is used to scrape the data from the Google Sheets and store it in the form of CSV files.

roastcalc.py takes those CSV files and looks at them to determine how much of each coffee to roast. This takes into account how much coffee we want to put on the shelves, how much was ordered, and the average percent loss for past roasts.

## USAGE:
* Make sure `history.csv` exists.
* `./scrape.py`
* `./roastcalc.py`

## TODO:
- [ ] Download the most recently available history.csv from scrape.py
- [ ] Create a way to fulfill orders
