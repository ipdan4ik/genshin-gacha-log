# genshin-gacha-log

This project made for providing easy way to track your gacha pulls in Genshin Impact.

## How it works
All your genshin gacha log is stored in json file. After executing `update_data.py`, the program takes your gacha data from game and adds it to that file. Please note that you need to enter the gacha history in game before executing the script.
The script `print_data_gsheet.py` prints your gacha log from json file to google sheet

This program uses `genshinstats` [module](https://github.com/thesadru/genshinstats)

## Configuration
1. Install `genshinstats` library
```pip install genshinstats"```
2. Rename `config.example.ini` to `config.ini`
3. Enter your user id (right bottom corner of the game screen) to `config.ini`
4. Log in to hoyolab.com
5. Enter language to `config.ini` (I tested my program only for `ru`)
6. Get your authkey:
    i. Open Paimon menu ingame
    ii. Click Feedback
    iii. Copy link from opened browser tab

## Using google sheets
1. Install the Google client library
`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
2. Create a blank google sheet and copy spreadsheet id to `config.ini` (it is the value after `https://docs.google.com/spreadsheets/d/`)
3. Rename or create a new tab named `main` in your google sheet
4. Run `print_data_gsheet.py`. If it is your first time running the script, it opens a new window prompting you to authorize in google
5. Well done, the program inserts gacha log in `main` tab. You may need to change columns width manually and add some style (it will not be changed after execution)
