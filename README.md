# genshin-gacha-log

This project made for providing easy way to track your gacha pulls in Genshin Impact.

## How it works
All your genshin gacha log is stored in json file. After executing `update_data.py`, the program takes your gacha data from game and adds it to that file. Please note that you need to enter the gacha history in game before executing the script.
The script `print_data_gsheet.py` prints your gacha log from json file to google sheet

This program uses `genshinstats` [module](https://github.com/thesadru/genshinstats)

## Configuration
1. Install `genshinstats` library
```pip install genshinstats"```
2. Rename `config.example.ini` to `config.iin`
3. Enter your user id (right bottom corner of the game screen) to `config.ini`
4. Get your `cookie_token` and `account_id` from hoyolab.com:
    1. Go to `hoyolab.com` and login
    2. Press `F12`
    3. Go to `Application`, `Cookies`, `https://www.hoyolab.com`
    4. Copy `cookie_token` and `account_id` to file `config.ini` (never share your token, it resets after changing password)
5. Enter language to `config.ini` (I tested program only for `ru`)

## Using google sheets
1. Install the Google client library
`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
2. Create a blank google sheet and copy spreadsheet id to `config.ini` (it is the value after `https://docs.google.com/spreadsheets/d/`)
3. Run `print_data_gsheet.py`. If it is your first time running the script, it opens a new window prompting you to authorize in google
4. Well done, the program creates a `main` tab and inserts gacha log there. You may need to change columns width manually and add some style (it will not be changed after execution)
