import json
import pandas as pd
import seaborn as sns
import pandas as pd
import seaborn as sns
import discord
import matplotlib.pyplot as plt
from discord.ext import commands
import matplotlib as mpl
from PIL import Image
from creds import token

f = open('maps.json')
maps = json.load(f)

ff = open('666.json')
match = json.load(ff)

callouts = []
mapName = []
locX = []
locY = []

xMultiplier = 0
yMultiplier = 0
xScalarToAdd = 0
yScalarToAdd = 0
for spot in range(len(maps['data'][0]['callouts'])):
    callouts.append(maps['data'][0]['callouts'][spot]['superRegionName'] +
                    ' '+maps['data'][0]['callouts'][spot]['regionName'])
    locX.append(maps['data'][0]['callouts'][spot]['location']['x'])
    locY.append(maps['data'][0]['callouts'][spot]['location']['y'])
    mapName.append(maps['data'][0]['displayName'])
    xMultiplier = maps['data'][0]['xMultiplier']
    yMultiplier = maps['data'][0]['yMultiplier']
    xScalarToAdd = maps['data'][0]['xScalarToAdd']
    yScalarToAdd = maps['data'][0]['yScalarToAdd']

ascentData = pd.DataFrame(
    {'Map': mapName, 'Callouts': callouts, 'X': locX, 'Y': locY})
ascentData['X'] = [ascentData['X'].iloc[i] *
                   xMultiplier+xScalarToAdd for i in ascentData.index]
ascentData['Y'] = [ascentData['Y'].iloc[i] *
                   yMultiplier+yScalarToAdd for i in ascentData.index]


victim=[]
killer=[]

for kill in range(len(match['data'][0]['kills'])):
    victim.append(match['data'][0]['kills'][kill]['victim_display_name'])
    killer.append(match['data'][0]['kills'][kill]['killer_display_name'])
killer_victim=pd.DataFrame(
    {'Killer': killer, 'Victim': victim})
print(killer_victim['Victim'].value_counts().keys()[0])
    
    
    




