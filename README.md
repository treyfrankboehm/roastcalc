# roastcalc

## ABOUT:
scrape.py is used to scrape the data from the Google Sheets and store it in the form of CSV files.

roastcalc.py takes those CSV files and looks at them to determine how much of each coffee to roast. This takes into account how much coffee we want to put on the shelves, how much was ordered, and the average percent loss for past roasts.

## USAGE:
* Make sure `history.csv` exists.
* [Edit](https://docs.google.com/spreadsheets/d/12McXQu2Ap7cRrX8U4Vegjk3zA3pPUd5HTLOp3swbswU/edit?usp=sharing) _Orders_ sheet to suit the day's needs.
* `./scrape.py`
* `./roastcalc.py`

## TODO:
- [ ] Download the most recently available `history.csv` using `scrape.py`
- [ ] Track and fulfill orders as they occur
- [ ] Email the roast needs to relevant members
- [ ] Subscription tracking
- [ ] Increased automation?
- [ ] Better user-friendliness (through automation)
- [ ] Change _Master_ spreadsheet sharing, remove `client_secret.json` for security (though I doubt this would ever be an issue)
