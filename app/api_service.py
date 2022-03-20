from api import ValorantAPI
from utils import logger
import pandas as pd
from typing import Optional, Tuple, Dict
import json
import discord
import glob
from pymongo import MongoClient
import time
from discord import Embed
from discord.ext import commands
from creds import token
from threading import Timer
import matplotlib.pyplot as plt
import matplotlib
import requests
import json
import pandas as pd
import seaborn as sns
import discord
import matplotlib.pyplot as plt
from discord.ext import commands
import matplotlib as mpl
from PIL import Image
from creds import token
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import json
import pandas as pd
from discord import Embed


class ApiService:

    QueueTypes = ('competitive', 'unrated', 'custom')

    def __init__(self, region):
        self.api = ValorantAPI(region=region)
        self.puuid: Optional[str] = None
        self.is_authed: bool = False

    @staticmethod
    def get_regions() -> Tuple[str]:
        return ValorantAPI.Regions

    def set_region(self, region: str):
        self.api.set_region_and_shard(region)
        logger.debug(
            f'Current region: {self.api.region} | Shard: {self.api.shard}')

    def try_auth(self) -> bool:
        self.puuid, _ = self.api.get_auth(force=True, cache_headers=True)
        if self.puuid is not None:
            self.is_authed = True
            return True
        return False

    # def get_maps_info(self):
    #     self.maps = {}
    #     maps_info = self.api.get_maps()
    #     for map_info in maps_info:
    #         self.maps[map_info['mapId']] = map_info

    def needs_auth(func):
        def wrapper(self, *args, **kwargs):
            if not self.is_authed:
                raise RuntimeWarning('Currently not authorized!')
            return func(self, *args, **kwargs)
        return wrapper

    @needs_auth
    def get_full_username(self, puuid: str) -> Optional[str]:
        names = self.api.get_names_from_puuids(puuid)
        return names[0] if names else None

    @needs_auth
    def get_all_match_history(self, puuid: str, queue: str):
        return self.api.get_all_match_history(puuid, queue=queue)

    @needs_auth
    def get_match_info(self, match_id: str) -> Dict:
        return self.api.get_match_info(match_id)


def getLastcountXMatch(tagName):

    # test.get_full_username(puuid='06790ed8-c5e5-5976-9767-98ea7ae3fbee')
    # matchList = test.get_all_match_history(
    # puuid='06790ed8-c5e5-5976-9767-98ea7ae3fbee', queue='custom')

    # with open('dataMatchList.json', 'w') as fp:
    #json.dump(test.get_all_match_history(puuid='06790ed8-c5e5-5976-9767-98ea7ae3fbee', queue='custom'), fp)

    # with open('data match'+str(i)+'.json', 'w') as fp:
    #json.dump(matchData, fp)

    client = MongoClient('127.0.0.1', 27017)
    matchDataDB = client["matchDataDB"]
    puuidTable = matchDataDB["puuid_with_name_matchdata"]

    fankos = pd.read_excel('fankos.xlsx')

    myquery = {"puuid":  fankos[fankos['name'] == tagName]['puuid'].iloc[0]}

    mydoc = puuidTable.find(myquery, {'Match_DATA': 1, "_id": False})
    kills = []
    deaths = []
    countX = 0
    for x in mydoc:

        for i in range(len(x['Match_DATA']['players'])):
            if x['Match_DATA']['players'][i]['subject'] == fankos[fankos['name'] == tagName]['puuid'].iloc[0]:
                kills.append(x['Match_DATA']['players'][i]['stats']['kills'])

                deaths.append(x['Match_DATA']['players'][i]['stats']['deaths'])
                countX += 1
    playerDF = pd.DataFrame({'Kills': kills, 'Deaths': deaths})
    kd = playerDF['Kills'].sum()/playerDF['Deaths'].sum()

    return kd, countX


def updateDB_newMatches():
    test = ApiService('EU')
    test.try_auth()
    client = MongoClient('127.0.0.1', 27017)
    matchDataDB = client["matchDataDB"]
    puuidTable = matchDataDB["puuid_with_name_matchdata"]
    fankos = pd.read_excel('fankos.xlsx')

    for i in fankos["puuid"]:
        lastMatch_matchID = test.get_all_match_history(puuid=i, queue='unrated')[
            'History'][0]['MatchID']

        myquery = {"puuid":  i, 'matchID': lastMatch_matchID}
        mydoc = puuidTable.find_one(myquery, {'Match_DATA': 1, "_id": False})
        if mydoc:
            pass
        else:
            matchData = test.get_match_info(match_id=lastMatch_matchID)
            puuidTable.insert_one(
                {'puuid': i, 'matchID': lastMatch_matchID, 'Match_DATA': matchData})
        time.sleep(15)


def get_Map(tagName):
    test = ApiService('EU')
    test.try_auth()
    client = MongoClient('127.0.0.1', 27017)

    matchDataDB = client["matchDataDB"]
    puuidTable = matchDataDB["puuid_with_name_matchdata"]
    fankos = pd.read_excel('fankos.xlsx')
    myquery = {"puuid":  fankos[fankos['name'] == tagName]['puuid'].iloc[0]}
    mydoc = puuidTable.find(myquery, {'Match_DATA': 1, "_id": False})

    # if x['Match_DATA']['matchInfo']['mapId'].contains('Ascent'):
    img = plt.imread("ascent.png")
    map_file = open('ascent.json')
    mapGame = json.load(map_file)

    zones = []
    x_a = []
    x_y = []
    x_test = []
    y_test = []
    xMultiplier = mapGame['multiplier']['x']
    yMultiplier = mapGame['multiplier']['y']
    xOffset = mapGame['offset']['x']
    yOffset = mapGame['offset']['y']
    for zone in range(len(mapGame['zones'])):

        for i in range(len(mapGame['zones'][zone]['points'])):
            zones.append(mapGame['zones'][zone]['name'])
            x_value = (mapGame['zones'][zone]['points'][i]['x'])
            y_value = (mapGame['zones'][zone]['points'][i]['y'])
            x_a.append(x_value)
            x_a.append(y_value)
            x_test.append(x_value)
            y_test.append(y_value)
            x_y.append(x_a)
            x_a = []

    ascent_map = pd.DataFrame({'Coords': x_y, 'Zone': zones})

    fig, ax = plt.subplots()
    ax.set_facecolor('black')
    for elem in set(ascent_map['Zone']):
        y = list(ascent_map[ascent_map['Zone'] == elem]['Coords'])

        p = Polygon(y, facecolor='white', alpha=0.15,
                    edgecolor='black', linewidth=0)
        # (0.5, 0.5)
        # if elem == 'Defender Spawn' or elem == 'Attacker Spawn':
        #ax.annotate(elem, xy=centroid(y), fontsize=5, color='black')
        ax.add_patch(p)
    for matchPlayed in mydoc:

        if matchPlayed['Match_DATA']['matchInfo']['mapId'].find('/Game/Maps/Ascent/Ascent'):
            for kill in range(len(matchPlayed['Match_DATA']['kills'])):
                if matchPlayed['Match_DATA']['kills'][kill]['victim'] == fankos[fankos['name'] == tagName]['puuid'].iloc[0]:

                    first_kill_location_x = (
                        matchPlayed['Match_DATA']['kills'][kill]['victimLocation']['y'])*xMultiplier+xOffset

                    first_kill_location_y = (
                        matchPlayed['Match_DATA']['kills'][kill]['victimLocation']['x'])*yMultiplier+yOffset

                plt.scatter(first_kill_location_x, 1 -
                            first_kill_location_y, c='red', marker='x')
            for kill in range(len(matchPlayed['Match_DATA']['kills'])):
                if matchPlayed['Match_DATA']['kills'][kill]['killer'] == fankos[fankos['name'] == tagName]['puuid'].iloc[0]:

                    first_kill_location_x = (
                        matchPlayed['Match_DATA']['kills'][kill]['victimLocation']['y'])*xMultiplier+xOffset
                    first_kill_location_y = (
                        matchPlayed['Match_DATA']['kills'][kill]['victimLocation']['x'])*yMultiplier+yOffset

                plt.scatter(first_kill_location_x, 1 -
                            first_kill_location_y, c='green', marker='o')

    plt.axis('off')

    ax.set_xlim(min(x_test), max(x_test))
    ax.set_ylim(min(y_test), max(y_test))

    ax.imshow(img, extent=[round(min(x_test)), round(
        max(x_test)), round(min(y_test)), round(max(y_test))])
    playerName = tagName.split('#')
    ax.set_title(
        playerName[0]+"'s Kills and Deaths Ascent", color='white')

    plt.savefig('mapStats.png', bbox_inches='tight',
                facecolor='black', dpi=600)
    plt.show()


client = discord.Client()


@client.event
async def on_ready():

    print("Le bot est prêt !")


@client.event
async def on_message(message):

    if message.content.startswith('.lastunratedStats'):
        messageWithoutstats = message.content.replace(".lastunratedStats ", "")

    kd, countX = getLastcountXMatch(messageWithoutstats)
    await message.channel.send('KD for your last '+str(countX)+' games')
    await message.channel.send("{:.2f}".format(kd))
    # await message.channel.send('**Kills/Deaths Ratio / Heashots**')
    # await message.channel.send(file=discord.File('merged_image1.jpg'))
    # await message.channel.send('**Total Damage / Ultimate Casts**')
    # await message.channel.send(file=discord.File('merged_image2.jpg'))

updateMatchesThreading = Timer(60.0, updateDB_newMatches)
updateMatchesThreading.start()

client.run(token)


# for file in glob.glob("*.json"):
#f = open(file)
#data = json.load(f)

# for i in range(len(data['players'])):
# if data['players'][int(i)]['subject'] in fankospuuid:
# pass
# else:

# Database creation
#fankos = pd.read_excel('fankos.xlsx')


# for j in range(len(matchList['History'])):
# try:


#puuidTable.insert_one({'puuid': i, 'matchID': matchList['History'][j]['MatchID'], 'Match_DATA': matchData})
# except:
# print(matchData)
#print(i, j)
# time.sleep(45)
