# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 12:51:43 2020

@author: Dillon Morse
"""

import folium
import pandas as pd
import numpy as np
import GetCircleCenters as CC
import Dataframe_clean_functions as clean
import Label_Boulder as cluster
import Process_and_Cluster as process
import matplotlib.cm as cm
import matplotlib.colors as colors

# =============================================================================
# Create map centered at these coordinates
# =============================================================================
lat = 40.019824
lng = -105.262982
map_Boulder = folium.Map(location=[lat, lng], zoom_start=12)


# =============================================================================
# Read in both city data and list of all region-centers (called 'markers' in
# the map context). Remove those markers which don't show up in the city data
# (i.e. due to too-low a venue population in the region)
# =============================================================================
Boulder_labels = cluster.Label_Boulder()
Boulder_labeled = process.Boulder_features().iloc[:,-2:]
Boulder_labeled['Label'] = Boulder_labels

marker_centers = CC.build_Boulder_circle_centers()
surviving_centers = [marker_centers[k] for k in Boulder_labeled['CircleNum'].unique() ]

radius = 500

Boulder_labeled['Center'] = surviving_centers

num_clusters = len( Boulder_labeled['Label'].unique() )
x = np.arange( num_clusters )
ys = [i + x + (i*x)**2 for i in range(num_clusters)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

for k in Boulder_labeled.index:
    lnglat = Boulder_labeled.loc[k,'Center']
    Label = Boulder_labeled.loc[k,'Label']
    (folium.Circle( lnglat,
                    radius = radius,
                    fill = True,
                    color = rainbow[Label],
                    weight = 1
                    )
           .add_to(map_Boulder)
           )

map_Boulder.save('Boulder_map.html')

def make_map():
    return map_Boulder