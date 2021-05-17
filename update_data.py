def get_new_gacha_data(account_id, token, uid, lang='ru'):
    import genshinstats as gs
    import json

    gs.set_cookie(ltoken=token, ltuid=account_id)

    data_dict = {}
    for t in gs.get_gacha_types(lang=lang):
        data_list = []
        for pull in gs.get_gacha_log(t['key'], lang='ru'):
            data_list.append(pull)
        data_list.reverse()
        data_dict[t['key']] = data_list
    json.dump(data_dict, open('data\\[%s]new_data.json'%(uid), 'w', encoding='utf-8'), ensure_ascii=False, indent='    ')
    return data_dict


def get_old_gacha_data(uid, lang='ru'):
    import os
    import json
    import genshinstats as gs
    data = {}
    if os.path.exists('data\\[%s]last_data.json'%(uid)) and os.stat('data\\[%s]last_data.json'%(uid)).st_size > 0:
        data = json.load(open('data\\[%s]last_data.json'%(uid), 'r', encoding='utf-8'))
    else:
        for t in gs.get_gacha_types(lang=lang):
            data[t['key']] = []
    return data


def compare_gacha_data(old_data_dict, new_data_dict):
    keys = set(new_data_dict.keys()) | set(old_data_dict.keys())
    final_list = {}
    
    for key in keys:
        i = 0
        j = 0
        ilen = len(old_data_dict[key])-1
        jlen = len(new_data_dict[key])-1
        final = []
        while ((i<=ilen) or (j<=jlen)):
            if (i>ilen):
                final.append(new_data_dict[key][j])
                ## print('[+] %s' %(new_data_dict[key][j]))
                j+=1
            elif (j>jlen):
                final.append(old_data_dict[key][i])
                # print('[+] %s' %(old_data_dict[key][i]))
                i+=1
            elif (old_data_dict[key][i] == new_data_dict[key][j]):
                final.append(old_data_dict[key][i])
                # print('[+] %s' %(old_data_dict[key][i]))
                i+=1
                j+=1
            elif (old_data_dict[key][i]['time'] == new_data_dict[key][j]['time']):
                final.append(old_data_dict[key][i])
                i+=1
                # print('[+] %s' %(old_data_dict[key][i]))
            elif (old_data_dict[key][i]['time'] > new_data_dict[key][j]['time']):
                final.append(new_data_dict[key][j])
                ## print('[+] %s' %(new_data_dict[key][j]))
                j+=1
            elif (old_data_dict[key][i]['time'] < new_data_dict[key][j]['time']):
                final.append(old_data_dict[key][i])
                # print('[+] %s' %(old_data_dict[key][i]))
                i+=1
        final_list[key] = final
        
    return final_list


def update_gacha_data():
    from config import GenshinConfig
    import json
    import os

    config = GenshinConfig('config.ini')
    account_id = config.account_id
    cookie_token = config.cookie_token
    user_id = config.user_id
    lang = config.lang
    new_data = get_new_gacha_data(account_id, cookie_token, user_id, lang)
    old_data = get_old_gacha_data(user_id, lang)
    final_data = compare_gacha_data(old_data, new_data)
    json.dump(final_data, open('data\\[%s]last_data.json'%(user_id), 'w', encoding='utf-8'), ensure_ascii=False, indent='    ')
    return final_data

if __name__ == "__main__":
    update_gacha_data()