#!/usr/bin/env python3

# This file is part of roastcalc
# 
# roastcalc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more detail.
# <http://www.gnu.org/licenses/>
#
# You should have received a copy of the GNU General Public License
# along with roastcalc.  If not, see <http://www.gnu.org/licenses/>.

import httplib2
import os
import apiclient
import oauth2client

# Most of this code is based on quickstart.py from the official Google
# page for the Sheets API. The values of interest are spreadsheetId and
# sheetNames.
spreadsheetId = "12McXQu2Ap7cRrX8U4Vegjk3zA3pPUd5HTLOp3swbswU"
sheetNames = {
        "products.csv":"Products",
#        "current.csv":"Current Stock",
#        "desired.csv":"Desired Stock",
#        "orders.csv":"Orders",
        "subscriptions.csv":"Subscriptions",
        "totals.csv":"Totals"
}
credentialPath= "sheets.googleapis.com-roastcalc.json"
clientSecret  = "client_secret.json"
scopes        = "https://www.googleapis.com/auth/spreadsheets.readonly"
application   = "roastcalc via Google Sheets API v4 for Python"

def get_credentials():
    # Gets new credentials, if needed, based on client_secret.json
    store = oauth2client.file.Storage(credentialPath)
    credentials = store.get()
    if not credentials or credentials.invalid:
        print("Credentials non-existent or invalid. Creating anew.")
        flow = oauth2client.client.flow_from_clientsecrets(
            clientSecret, scopes)
        flow.user_agent = application
        credentials = oauth2client.tools.run_flow(flow, store)
        print("Storing credentials to " + credentialPath)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ("https://sheets.googleapis.com/$discovery/rest?"
            "version=v4")
    service = apiclient.discovery.build("sheets", "v4", http=http, discoveryServiceUrl=discoveryUrl)

    for fileName in sheetNames:
        rangeName = sheetNames[fileName]
        result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId, range=rangeName).execute()
        values = result.get("values", [])

        if not values:
            sys.stderr.write("error: No data found.")
        else:
            # Write the values to a CSV file
            del(values[0]) # Delete sheet header
            f = open(fileName,"w")
            for row in values:
                f.write("%s\n" % ",".join(row))
            f.close
            print("Scraped data into %s." % fileName)

if __name__ == "__main__":
    main()
