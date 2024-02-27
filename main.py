import urllib.request, json
from howlongtobeatpy import HowLongToBeat
import re
import xlsxwriter
import os

user_id = "XXXXXXXXXXX"
webapi_key = ""

workbook = xlsxwriter.Workbook('Games.xlsx')
worksheet = workbook.add_worksheet()
with urllib.request.urlopen("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + webapi_key + "&steamid="+ user_id + "&format=json&include_appinfo=true&include_played_free_games=false") as url:

    data = json.load(url)["response"]
    print("User has " + str(data["game_count"]) + " games.")
    game_amount = data["game_count"]
    for i in range(len(data["games"])):
        with urllib.request.urlopen("http://steamspy.com/api.php?request=appdetails&appid=" + str(data["games"][i]["appid"])) as game_url:
            game_data = json.load(game_url)
            if(game_data["price"] == 0): continue
        game_name_raw = data["games"][i]["name"]
        #game_name_clean = re.sub(r"[^a-zA-Z0-9]+", ' ', game_name_raw)
        game_name_clean = game_name_raw.replace('™', '')
        game_name = game_name_clean.lower()
        game_length_results = HowLongToBeat().search(game_name)
        game_length = 0
        if(len(game_length_results) > 0):
            game_length = game_length_results[0].main_story
        #print(game_name + ": " + str(game_length))
        worksheet.write(i, 0, game_name_raw)
        worksheet.write(i, 1, game_length)
        if(len(game_length_results) > 0):
            worksheet.write(i, 2, "https://howlongtobeat.com/game/" + str(game_length_results[0].game_id))
        progress = 0
        if(i > 0):
            progress = (i / game_amount) * 100
        os.system("cls")
        print("Current progress: " + str(game_amount) + "/" + str(i) + ", " + str(round(progress, 2)) + "%")

workbook.close()

#print(HowLongToBeat().search()[0].main_story)