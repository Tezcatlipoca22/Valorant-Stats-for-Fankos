from turtle import color
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import json
import pandas as pd





ascent = json.load(ff)

ascent_map.to_excel('audit.xlsx')
        

def centroid(vertexes):
     _x_list = [vertex [0] for vertex in vertexes]
     _y_list = [vertex [1] for vertex in vertexes]
     _len = len(vertexes)
     _x = sum(_x_list) / _len
     _y = sum(_y_list) / _len
     return(_x, _y)
        


# points = ((1,1), (2,1), (2,2), (1,2), (0.5,1.5))
fig,ax = plt.subplots()
ax.set_facecolor('white')
patches=[]
for elem in set(ascent_map['Zone']):
    y=list(ascent_map[ascent_map['Zone']==elem]['Coords'])
    
    p = Polygon(y, facecolor = 'red', alpha=0.2, edgecolor='black', linewidth=1)
    centroid(y) # (0.5, 0.5)
    
    ax.add_patch(p)
    
    
    
    
plt.show()









    
    



    

