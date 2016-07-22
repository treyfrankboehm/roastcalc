#!/usr/bin/env python3

# Most of this code was taken from quickstart.py on the official Google
# page for the Sheets API.
# The values of interest are spreadsheetId and rangeName. Change these
# to suit the needs of the program.


from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'roastcalc.py via Google Sheets API Python'


def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
    Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
            'sheets.googleapis.com-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.useragent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
            'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    spreadsheetId = '12McXQu2Ap7cRrX8U4Vegjk3zA3pPUd5HTLOp3swbswU'
    sheetNames = {'single.csv':'Single Origin', 'blends.csv':'Blends', 'orders.csv':'Orders', 'stock.csv':'Stock' }

    for fileName in sheetNames:
        rangeName = sheetNames[fileName]
        result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheetId, range=rangeName).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            del(values[0]) # Spreadsheet header
            f = open(fileName,"w")
            for row in values:
                f.write("%s\n" % ','.join(row))
            f.close

if __name__ == "__main__":
    main()
