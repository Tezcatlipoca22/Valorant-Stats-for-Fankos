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


def getMATCHHistory(name: str, tag: str, region: str, zed: int) -> dict:

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
        data_final.to_excel('data_final'+str(zed)+'.xlsx')

        # totalDamageRe = sns.barplot(data=data_final.sort_values(
        # by='Total Damage received', ascending=False), x='Joueur', y='Total Damage received', palette='Reds_r')
        #fig = totalDamageRe.get_figure()
        # plt.xticks(rotation=45)
        # fig.savefig("Total Damage Received"+str(zed) +
        # ".png", bbox_inches='tight')

ff = open('matchdata.json')
match = json.load(ff)
def get_Most_killed_player():
    
    victim = []
    killer = []
    for kill in range(len(match['data']['0']['kills'])):
        victim.append(match['data']['0']['kills'][kill]['victim_display_name'])
        killer.append(match['data']['0']['kills'][kill]['killer_display_name'])
    killer_victim = pd.DataFrame({'Killer': killer, 'Victim': victim})
    
    return str(killer_victim['Victim'].value_counts().keys()[0])


client = discord.Client()


@client.event
async def on_ready():
    print("Le bot est prêt !")


@client.event
async def on_message(message):

    if message.content.startswith('.lastgameStats'):
        messageWithoutstats = message.content.replace(".lastgameStats ", "")

        userData = messageWithoutstats.split('#')
        getMATCHHistory(name=userData[0], tag=userData[1], region='eu', zed=0)
        await message.channel.send('**Here are the last game stats of ' + userData[0]+'**')
        await message.channel.send('**Kills/Deaths Ratio / Heashots**')
        await message.channel.send(file=discord.File('merged_image1.jpg'))
        await message.channel.send('**Total Damage / Ultimate Casts**')
        await message.channel.send(file=discord.File('merged_image2.jpg'))
        await message.channel.send('**Most Killed Player (tamssoun) : '+get_Most_killed_player()+'**')

client.run(token)
