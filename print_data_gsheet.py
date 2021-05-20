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
    from config import GoogleConfig
    config = GoogleConfig('config.ini')
    spreadsheet_id = config.spreadsheet_id
    for i, row in enumerate(sheet_data):
        for j, item in enumerate(row):
            sheet_data[i][j] = str(sheet_data[i][j])
    service = connect_gsheet()
    body = {"majorDimension": majorDimension, 'values': sheet_data}
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=s_range, valueInputOption='RAW', body=body).execute()
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

def print_stats(data_dict):
    ranges = ['stats!A1', 'stats!G1']
    keys = list(data_dict.keys())
    keys.sort()
    gsheet_list = [['Название молитвы', 'Кол-во роллов', 'Кол-во 4★', 'Кол-во 5★', 'Последний ролл']]
    all_length = 0
    all_four = 0
    all_five = 0
    all_four_list = []
    all_five_list = []
    for key in keys:
        name = data_dict[key][0]['gacha_name']
        length = len(data_dict[key])
        four = 0
        five = 0
        last_4 = 1
        last_5 = 1
        four_list = []
        five_list = []
        for item in data_dict[key]:
            if item['rarity'] in ['4', 4]:
                four_list.append(last_4)
                four += 1
                last_4 = 0
            elif item['rarity'] in ['5', 5]:
                five_list.append(last_5)
                five += 1
                last_5 = 0
            last_4 += 1
            last_5 += 1
        all_length += length
        all_four += four
        all_five += five
        all_four_list.extend(four_list)
        all_five_list.extend(five_list)
        gsheet_list.append([name, length, four, five, last_5])
    gsheet_list.append(['Все', all_length, all_four, all_five])
    export_gsheet(gsheet_list, ranges[0])
    gsheet_list = [['', '4★', '5★']]
    gsheet_list.append(['Соотношение', str(all_four / all_length)[:8], str(all_five / all_length)[:8]])
    gsheet_list.append(['Среднее', str(all_length/all_four)[:8], str(all_length/all_five)[:8]])
    get_median = lambda x: (x[len(x) // 2] + x[~(len(x) // 2)]) / 2
    all_four_list.sort()
    all_five_list.sort()
    gsheet_list.append(['Медиана', get_median(all_four_list), get_median(all_five_list)])
    export_gsheet(gsheet_list, ranges[1])
        
def print_characters(cookie_token, account_id, user_id):
    import genshinstats as gs
    
    ranges = ['chars!A1']
    gsheet_list = [['Персонаж', 'Созвездие', 'Дружба', 'Уровень', 'Редкость']]
    gs.set_cookie(ltoken=cookie_token, ltuid=account_id)
    characters = gs.get_all_characters(user_id)

    for char in characters:
        gsheet_list.append([char['name'], char['constellation'], char['friendship'], char['level'], char['rarity']])
    export_gsheet(gsheet_list, ranges[0])

if __name__ == "__main__":
    import update_data as up
    from config import GenshinConfig
    config = GenshinConfig('config.ini')
    account_id = config.account_id
    cookie_token = config.cookie_token
    user_id = config.user_id
    data_dict = up.update_gacha_data()
    # data_dict = up.get_old_gacha_data(user_id)
    print_full_log(data_dict)
    print_stats(data_dict)
    print_characters(cookie_token, account_id, user_id)
