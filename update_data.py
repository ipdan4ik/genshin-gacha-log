def get_new_gacha_data(account_id, token, uid, lang='ru'):
    import genshinstats as gs
    import json
    from collections import OrderedDict

    gs.set_cookie(ltoken=token, ltuid=account_id)

    data_dict = OrderedDict()
    types = gs.get_gacha_types(lang=lang)
    keys = [item['key'] for item in types]
    keys.sort()
    for key in keys:
        data_list = []
        for pull in gs.get_gacha_log(key, lang='ru'):
            data_list.append(pull)
        data_list.reverse()
        data_dict[key] = data_list
    json.dump(data_dict, open('data\\[%s]new_data.json'%(uid), 'w', encoding='utf-8'), ensure_ascii=False, indent='    ')
    return data_dict


def get_old_gacha_data(uid, lang='ru'):
    import os
    import json
    import genshinstats as gs
    from collections import OrderedDict
    data = OrderedDict()
    if os.path.exists('data\\[%s]last_data.json'%(uid)) and os.stat('data\\[%s]last_data.json'%(uid)).st_size > 0:
        data = json.load(open('data\\[%s]last_data.json'%(uid), 'r', encoding='utf-8'))
    else:
        types = gs.get_gacha_types(lang=lang)
        keys = [item['key'] for item in types]
        keys.sort()
        for key in keys:
            data[key] = []
    return data


def compare_gacha_data(old_data_dict, new_data_dict):
    from collections import OrderedDict
    keys = set(new_data_dict.keys()) | set(old_data_dict.keys())
    keys = list(keys)
    keys.sort()
    final_list = OrderedDict()
    
    for key in keys:
        i = 0
        j = 0
        ilen = len(old_data_dict[key])-1
        jlen = len(new_data_dict[key])-1
        final = []
        while ((i<=ilen) or (j<=jlen)):
            if (i>ilen):
                final.append(new_data_dict[key][j])
                print('[+] %s' %(new_data_dict[key][j]))
                j+=1
            elif (j>jlen):
                final.append(old_data_dict[key][i])
                i+=1
            elif (old_data_dict[key][i] == new_data_dict[key][j]):
                final.append(old_data_dict[key][i])
                i+=1
                j+=1
            elif (old_data_dict[key][i]['id'] == new_data_dict[key][j]['id']):
                final.append(old_data_dict[key][i])
                i+=1
            elif (old_data_dict[key][i]['id'] > new_data_dict[key][j]['id']):
                final.append(new_data_dict[key][j])
                print('[+] %s' %(new_data_dict[key][j]))
                j+=1
            elif (old_data_dict[key][i]['id'] < new_data_dict[key][j]['id']):
                final.append(old_data_dict[key][i])
                i+=1
        final_list[key] = final
        
    return final_list


def update_gacha_data():
    from collections import OrderedDict
    from config import GenshinConfig
    import json
    import datetime

    config = GenshinConfig('config.ini')
    account_id = config.account_id
    cookie_token = config.cookie_token
    user_id = config.user_id
    lang = config.lang

    new_data = get_new_gacha_data(account_id, cookie_token, user_id, lang)
    old_data = get_old_gacha_data(user_id, lang)
    final_data = compare_gacha_data(old_data, new_data)
    date_now = datetime.datetime.strftime(datetime.datetime.now(), '%d.%m.%Y')
    json.dump(old_data, open('data\\[%s]last_data_backup[%s].json'%(user_id, date_now), 'w', encoding='utf-8'), ensure_ascii=False, indent='    ')
    json.dump(final_data, open('data\\[%s]last_data.json'%(user_id), 'w', encoding='utf-8'), ensure_ascii=False, indent='    ')
    return final_data

if __name__ == "__main__":
    update_gacha_data()