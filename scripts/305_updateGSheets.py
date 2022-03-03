from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
import pickle
import os.path

# 数値→アルファベット
def num2alpha(num):
    if num<=26:
        return chr(64+num)
    elif num%26==0:
        return num2alpha(num//26-1)+chr(90)
    else:
        return num2alpha(num//26)+chr(64+num%26)

"""
Shows basic usage of the Sheets API.
Prints values from a sample spreadsheet.
"""

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('../../token.pickle'):
    with open('../../token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('../../token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

spreadsheet_id = '1W2akkXwfDENiC78Cbx1qs3rx39RvIz4ZEGMio0ZMRYs'

config = {
    "item" : "item2",
    "div1" : "div1_2"
}

for key in config:

    df = pd.read_csv("data/{}.csv".format(key))

    columns_name = df.columns

    cols = []
    data = []
    for col in df.columns:
        cols.append(col)

    data.append(cols)

    for index, row in df.iterrows():
        row2 = []
        for col in df.columns:
            value = row[col]
            if pd.isnull(value):
                value = ""
            row2.append(value)

        data.append(row2)


    sheet_name = config[key]

    range_name = sheet_name+'!A1:'+str(num2alpha(len(cols)))+str(len(data))
    value_input_option = 'USER_ENTERED'
    values = data
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()

