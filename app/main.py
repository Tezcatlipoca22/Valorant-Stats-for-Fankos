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


def plotTotalDMG(dataFrameMatch):
    totalDamage = sns.barplot(data=dataFrameMatch.sort_values(
        by='Total Damage', ascending=False), x='Joueur', y='Total Damage', palette='Purples_r')
    figDMG = totalDamage.get_figure()
    totalDamage.set(title='Last game total Damage')
    plt.xticks(rotation=45)
    figDMG.savefig("Total Damage.png", bbox_inches='tight')
    plt.clf()


def plotTotalHeadshots(dataFrameMatch):
    totalHeadshots = sns.barplot(data=dataFrameMatch.sort_values(
        by='Headshots', ascending=False), x='Joueur', y='Headshots', palette='Reds_r')
    figHS = totalHeadshots.get_figure()
    totalHeadshots.set(title='Last game Headshots')
    plt.xticks(rotation=45)
    figHS.savefig("Total Headshots.png", bbox_inches='tight')
    plt.clf()


def plotKD(dataFrameMatch):
    totalKD = sns.barplot(data=dataFrameMatch.sort_values(
        by='KD', ascending=False), x='Joueur', y='KD', palette='Blues_r')
    figKD = totalKD.get_figure()
    totalKD.set(title='Last game Kills/Deaths R')
    plt.xticks(rotation=45)
    figKD.savefig("KD.png", bbox_inches='tight')
    plt.clf()


def plotUltUsage(dataFrameMatch):
    totalUlt = sns.barplot(data=dataFrameMatch.sort_values(
        by='Ultimate', ascending=False), x='Joueur', y='Ultimate', palette='Greens_r')
    figUlt = totalUlt.get_figure()
    totalUlt.set(title='Ultimate casts')
    plt.xticks(rotation=45)
    figUlt.savefig("Ultimate usage.png", bbox_inches='tight')
    plt.clf()


def mergeImg1():
    # Read the two images
    image1 = Image.open('KD.png')

    image2 = Image.open('Total Headshots.png')

    # resize, first image

    image1_size = image1.size
    image2_size = image2.size
    new_image = Image.new(
        'RGB', (2*image1_size[0], image1_size[1]), (250, 250, 250))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_size[0], 0))
    new_image.save("merged_image1.jpg", "JPEG")


def mergeImg2():
    # Read the two images
    image1 = Image.open('Total Damage.png')

    image2 = Image.open('Ultimate usage.png')

    # resize, first image

    image1_size = image1.size
    image2_size = image2.size
    new_image = Image.new(
        'RGB', (2*image1_size[0], image1_size[1]), (250, 250, 250))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1_size[0], 0))
    new_image.save("merged_image2.jpg", "JPEG")


def getMatchHistory(name: str, tag: str, region: str, zed: int) -> dict:

    valid_region = ['ap', 'br', 'eu', 'kr', 'latam', 'na']
    if region.lower() not in valid_region:
        raise ValueError(f'"{region}" is not a valid region!')
    else:
        r = requests.get(
            f'https://api.henrikdev.xyz/valorant/v3/matches/{region}/{name}/{tag}')
        r.encoding = 'utf-8'
        res = r.json()
        test = (pd.DataFrame(res))
        test.to_json('matchdata.json')
        matchMap = test['data'][0]['metadata']['map']
        names = []
        agents = []
        scores = []
        damage_made = []
        headshots = []
        damage_received = []
        kills = []
        deaths = []
        qCasts = []
        cCasts = []
        eCasts = []
        xCasts = []

        for i in range(0, 10):
            names.append(test['data'][zed]['players']
                         ['all_players'][i]['name'])
            agents.append(test['data'][zed]['players']
                          ['all_players'][i]['character'])
            scores.append(test['data'][zed]['players']
                          ['all_players'][i]['stats']['score'])
            damage_made.append(test['data'][zed]['players']
                               ['all_players'][i]['damage_made'])
            damage_received.append(
                test['data'][zed]['players']['all_players'][i]['damage_received'])
            headshots.append(test['data'][zed]['players']
                             ['all_players'][i]['stats']['headshots'])
            kills.append(test['data'][zed]['players']
                         ['all_players'][i]['stats']['kills'])
            deaths.append(test['data'][zed]['players']
                          ['all_players'][i]['stats']['deaths'])
            qCasts.append(test['data'][zed]['players']
                          ['all_players'][i]['ability_casts']['q_cast'])
            cCasts.append(test['data'][zed]['players']
                          ['all_players'][i]['ability_casts']['c_cast'])
            eCasts.append(test['data'][zed]['players']
                          ['all_players'][i]['ability_casts']['e_cast'])
            xCasts.append(test['data'][zed]['players']
                          ['all_players'][i]['ability_casts']['x_cast'])

        data_final = pd.DataFrame({'Joueur': names, 'Agent': agents, 'Scores': scores,
                                  'Total Damage': damage_made, 'Total Damage received': damage_received, 'Headshots': headshots, 'Kills': kills, 'Deaths': deaths, 'Ultimate': xCasts})
        data_final['KD'] = [data_final['Kills'].iloc[num] /
                            data_final['Deaths'].iloc[num] for num in range(0, 10)]
        plotTotalDMG(dataFrameMatch=data_final)
        plotTotalHeadshots(dataFrameMatch=data_final)
        plotKD(dataFrameMatch=data_final)
        plotUltUsage(dataFrameMatch=data_final)
        mergeImg1()
        mergeImg2()

        # totalDamageRe = sns.barplot(data=data_final.sort_values(
        # by='Total Damage received', ascending=False), x='Joueur', y='Total Damage received', palette='Reds_r')
        #fig = totalDamageRe.get_figure()
        # plt.xticks(rotation=45)
        # fig.savefig("Total Damage Received"+str(zed) +
        # ".png", bbox_inches='tight')


def get_Most_killed_player():
    ff = open('matchdata.json')
    match = json.load(ff)
    victim = []
    killer = []
    for kill in range(len(match['data']['0']['kills'])):
        victim.append(match['data']['0']['kills'][kill]['victim_display_name'])
        killer.append(match['data']['0']['kills'][kill]['killer_display_name'])
    killer_victim = pd.DataFrame({'Killer': killer, 'Victim': victim})

    return str(killer_victim['Victim'].value_counts().keys()[0])


def centroid(vertexes):
    _x_list = [vertex[0] for vertex in vertexes]
    _y_list = [vertex[1] for vertex in vertexes]
    _len = len(vertexes)
    _x = sum(_x_list) / _len
    _y = sum(_y_list) / _len
    return(_x, _y)


def get_Map(player):
    matchdata = open('matchdata.json')
    match = json.load(matchdata)
    map_name = match['data']['0']['metadata']['map']

    if map_name == 'Ascent':
        map_file = open('ascent.json')
        mapGame = json.load(map_file)
        img = plt.imread("ascent.png")
    elif map_name == 'Split':
        map_file = open('bonsai.json')
        mapGame = json.load(map_file)
        img = plt.imread("split.png")
    elif map_name == 'Breeze':
        map_file = open('foxtrot.json')
        mapGame = json.load(map_file)
        img = plt.imread("breeze.png")
    elif map_name == 'Fracture':
        map_file = open('canyon.json')
        mapGame = json.load(map_file)
        img = plt.imread("fracture.png")
    elif map_name == 'Haven':
        map_file = open('triad.json')
        mapGame = json.load(map_file)
        img = plt.imread("haven.png")
    elif map_name == 'Icebox':
        map_file = open('port.json')
        mapGame = json.load(map_file)
        img = plt.imread("icebox.png")
    elif map_name == 'Bind':
        map_file = open('duality.json')
        mapGame = json.load(map_file)
        img = plt.imread("bind.png")

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
        centroid(y)  # (0.5, 0.5)
        # if elem == 'Defender Spawn' or elem == 'Attacker Spawn':
        #ax.annotate(elem, xy=centroid(y), fontsize=5, color='black')
        ax.add_patch(p)
    ff = open('matchdata.json')
    match = json.load(ff)
    for kill in range(len(match['data']['0']['kills'])):
        if match['data']['0']['kills'][kill]['victim_display_name'] == player:

            first_kill_location_x = (
                match['data']['0']['kills'][kill]['victim_death_location']['y'])*xMultiplier+xOffset
            first_kill_location_y = (
                match['data']['0']['kills'][kill]['victim_death_location']['x'])*yMultiplier+yOffset

            plt.scatter(first_kill_location_x, 1 -
                        first_kill_location_y, c='red', marker='x')
    for kill in range(len(match['data']['0']['kills'])):
        if match['data']['0']['kills'][kill]['killer_display_name'] == player:

            first_kill_location_x = (
                match['data']['0']['kills'][kill]['victim_death_location']['y'])*xMultiplier+xOffset  # swaping x and y
            first_kill_location_y = (
                match['data']['0']['kills'][kill]['victim_death_location']['x'])*yMultiplier+yOffset

            plt.scatter(first_kill_location_x, 1 -  # y=1-y to get the precise location
                        first_kill_location_y, c='green', marker='o')

    plt.axis('off')

    ax.set_xlim(min(x_test), max(x_test))
    ax.set_ylim(min(y_test), max(y_test))

    ax.imshow(img, extent=[round(min(x_test)), round(
        max(x_test)), round(min(y_test)), round(max(y_test))])
    playerName = player.split('#')
    ax.set_title(
        playerName[0]+"'s Kills and Deaths ("+map_name+")", color='white')

    plt.savefig('mapStats.png', bbox_inches='tight',
                facecolor='black', dpi=600)
    plt.clf()


client = discord.Client()


@client.event
async def on_ready():
    print("Le bot est prêt !")


@client.event
async def on_message(message):

    if message.content.startswith('.lastgameStats'):
        messageWithoutstats = message.content.replace(".lastgameStats ", "")

        userData = messageWithoutstats.split('#')
        getMatchHistory(name=userData[0], tag=userData[1], region='eu', zed=0)
        await message.channel.send('**Here are the last game stats of ' + userData[0]+'**')
        await message.channel.send('**Kills/Deaths Ratio / Heashots**')
        await message.channel.send(file=discord.File('merged_image1.jpg'))
        await message.channel.send('**Total Damage / Ultimate Casts**')
        await message.channel.send(file=discord.File('merged_image2.jpg'))

        get_Map(messageWithoutstats)
        await message.channel.send("**Your kills and deaths**")
        await message.channel.send(file=discord.File('mapStats.png'))


client.run(token)
