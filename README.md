# roastcalc

## ABOUT:
`scrape.py` is used to scrape the data from the Google Sheets and store it in the form of CSV files.

`roastcalc.py` takes those CSV files and looks at them to determine how much of each coffee to roast. This takes into account how much coffee we want to put on the shelves, how much was ordered, and the average percent loss for past roasts.

Before running, [edit](https://docs.google.com/spreadsheets/d/12McXQu2Ap7cRrX8U4Vegjk3zA3pPUd5HTLOp3swbswU/edit?usp=sharing) _Orders_ sheet to suit the day's needs, _Current Stock_ to reflect what's on the shelves and in bulk bags, and _Subscriptions_, if applicable. Regularly check to make sure that _Products_ accurately reflects the currently-offered products and that _Desired Stock_ represents the ideal amount of coffees on the shelf. _Totals_ will be automatically generated, but make sure that the list of products in column A is consistent across all sheets.

## DEPENDENCIES:
- [ ] python3
- [ ] httplib2 (python module)
- [ ] apiclient (python module)
- [ ] oauth2client (python module)
- [ ] bsd-mailx (set `emailBool` to `False` if you don't want to use this feature)

## USAGE:
* Make sure `history.csv` exists.
* [Edit](https://docs.google.com/spreadsheets/d/12McXQu2Ap7cRrX8U4Vegjk3zA3pPUd5HTLOp3swbswU/edit?usp=sharing) the spreadsheet as needed.
* Download a `client_secret.json` file from 
* `./roastcalc.py`

## TODO:
- [ ] Download the most recently available `history.csv` using `scrape.py` (need to look into Cropster functions/capabilities)
- [ ] Track and fulfill orders as they occur (this may be a different tool altogether)
- [ ] Easier way to set up the script on a new computer. Dependency list, google API key generation, cross-platform functionality.
