

if __name__ == "__main__":
    import update_data as up
    data_dict = up.get_old_gacha_data(700052434)
    keys = list(data_dict.keys())
    keys.sort()
    key = keys[0]
    with open('html.html', 'w', encoding='utf-8') as html_file:
        html_file.write(f'''
        <table> 
        <tr> <td colspan=4 align="center"> {data_dict[key][0]['gacha_name']} </td> <tr>
            <tr>
                <th>#</th>
                <th>##</th> 
                <th>Name</th> 
                <th>Date</th> 
            </tr>
            
        ''')
        j = 0
        for i, item in enumerate(data_dict[key]):
            html_file.write(f'''
                <tr>
                    <td>{i+1}</td>
                    <td>{j}</td> 
                    <td>{item['name']}</td> 
                    <td>{item['time']}</td> 
                </tr>
            ''')
            if item['rarity'] in [5, '5']:
                j = 0
            j+=1
        html_file.write(f'''
        </table>    
        ''')