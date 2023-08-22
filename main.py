# // https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=86E1078E76C768C46B2B204BEDB3B009&steamid=<userid>&relationship=friend


#Imports

import requests
import json
from bs4 import BeautifulSoup
import lxml
import time

def gettingData():

    #Steam ID array
    FriendsteamID = []
    elo = []
    name = []
    payload = {}
    headers = {
        'Authorization': 'config.API',
        'Cookie': '__cf_bm=94XrtyyRrKkCCQKrx3US_HX2mIwdUZWjyVyAfRLY_SQ-1668382598-0-AXE4gj/D7eJkmP4HnS46YB5xv3N1faeginQYWoe2TBbLSjgmDyXIE9Nw2Pt8xw5bdZ/1M9baT5ApQ/a/9878IRw=; __cfruid=c450454ab4ec480fae9bf3af2ff265d89e5f395d-1668382598'
    }

    steamID = input("Enter the desired users steam 64 ID E.G 76561198259409483")
    convertedID = str(steamID)
    apiCallSteamIDS = str("https://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=86E1078E76C768C46B2B204BEDB3B009&steamid="+ convertedID +"&relationship=friend")
    response = requests.get(apiCallSteamIDS)

    responseJSON = response.json()

    for i in range(len(responseJSON['friendslist']['friends'])):
        FriendsteamID.append(responseJSON['friendslist']['friends'][i]['steamid'])

    start = time.time()
    s = requests.Session()

    #Getting highest level player
    for i in range(len(FriendsteamID)):
        URL = "https://open.faceit.com/data/v4/players?game=csgo&game_player_id=" +FriendsteamID[i]

        response2 = s.request("GET", URL, headers=headers, data=payload)

        response2JSON = response2.json()
        print("Retreiving {0} out of {1} friend(s)".format(i, len(FriendsteamID)))
        try:
            eloVal = response2JSON['games']['csgo']['faceit_elo']
            elo.append(eloVal)
        except:
            print("No faceit account with csgo elo")

        try:
            nameVal = response2JSON['games']['csgo']['game_player_name']
            name.append(nameVal)
        except:
            print("No faceit account with csgo")
    end = time.time()
    total_time = end - start
    print("Total time taken = " + str(total_time) + " seconds")
    gettingHighestElo(elo,name)


def gettingHighestElo(elo, name):

    maxElo = 0
    maxName = ""

    for i in range(len(elo)):
        if elo[i] > maxElo:
            maxElo = elo[i]
            maxName = name[i]

    print("Highest elo player is {0} with {1} elo".format(maxName, maxElo))



if __name__ == '__main__':

    gettingData()


