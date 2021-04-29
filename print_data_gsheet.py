from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

def connect_gsheet():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
    if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return(service)

def export_gsheet(sheet_data, s_range, majorDimension='ROWS'):
    import gsheets_config as conf
    for i, row in enumerate(sheet_data):
        for j, item in enumerate(row):
            sheet_data[i][j] = str(sheet_data[i][j])
    service = connect_gsheet()
    body = {"majorDimension": majorDimension, 'values': sheet_data}
    result = service.spreadsheets().values().update(spreadsheetId=conf.spreadsheet_id, range=s_range, valueInputOption='RAW', body=body).execute()
    print('{0} cells updated'.format(result.get('updatedCells')))
    return(result)

def print_full_log(data_dict):
    ranges = ['main!A1', 'main!G1', 'main!M1', 'main!S1']
    rid = 0
    keys = list(data_dict.keys())
    keys.sort()

    for key in keys:
        gsheet_list = []
        gsheet_list.append([data_dict[key][0]['gacha_name']])
        gsheet_list.append(['#', '5#', 'name', 'time', 'rarity'])
        j = 1
        for i, item in enumerate(data_dict[key]):
            gsheet_list.append([i+1, j, item['name'], item['time'], item['rarity']])
            if item['rarity'] in [5, '5']:
                j = 0
            j+=1
        export_gsheet(gsheet_list, ranges[rid])
        rid+=1

if __name__ == "__main__":
    import update_data as up
    data_dict = up.update_gacha_data()
    print_full_log(data_dict)
