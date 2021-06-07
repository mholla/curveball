#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 18:39:29 2021

@author: nagehan
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import scipy.stats as stats
from matplotlib import colors
import statistics
from scipy.stats import skew

input_txt = 'subjects_Yale_TD.txt'
path = os.path.join(os.getcwd(),input_txt)
with open(path) as f: lines = f.read().splitlines()

SI_all = []

for line in lines:
    
    hemis = ['lh','rh']
        
    for hemi in hemis:
    
        SI = '{h}.pial.SI.asc'.format(h=hemi)
        
        subjects_name = 'Yale_vtk'
        subjects_dir = os.path.join(os.getcwd(),subjects_name)
        subject = '{l}'.format(l=line)
        
        SI = os.path.join(subjects_dir, subject, 'surf', SI)
            
       # reading shape index
        with open(SI,'r') as SI_file:
            SI_lines = SI_file.readlines()
            
        SI = np.zeros(len(SI_lines))
            
        for i in range(len(SI_lines)):
            SI_data = SI_lines[i].split()
            SI[i] = SI_data[4]
        
        SI = SI[SI != 0]
        
        SI_all = np.append(SI_all, SI)
    
#Colormap viridis histplot
    
kde = stats.gaussian_kde(SI_all)
# N is the count in each bin, bins is the lower-limit of the bin
N, bins, patches = plt.hist(SI_all, bins=50, density=True)

# We'll color code by height, but you could use any scalar
fracs = -np.linspace(min(SI_all), max(SI_all), 50)
xx = np.linspace(min(SI_all), max(SI_all), 1000)

# we need to normalize the data to 0..1 for the full range of the colormap
norm = colors.Normalize(fracs.min(), fracs.max())

# Now, we'll loop through our objects and set the color of each accordingly
for thisfrac, thispatch in zip(fracs, patches):
    color = plt.cm.viridis(norm(thisfrac))
    thispatch.set_facecolor(color)
    
plt.plot(xx, kde(xx), color='gray')
plt.show()

fig, ax = plt.subplots()
sns.distplot(-SI_all, bins=30, hist=True, norm_hist=True, color='#3E4A89', hist_kws={'edgecolor':'white'}, kde_kws={'linewidth': 2})
plt.show()

plt.figure()
sns.kdeplot(-SI_all, color='#3E4A89', shade=True, label='Pos k1, k2')
plt.show()


#Statistics
var = statistics.variance(SI_all)
var = np.var(SI_all)
mean = np.mean(SI_all)
skew = skew(SI_all)
mode = statistics.mode(SI_all)

import pandas as pd

dataVal = H_all
dataFrame = pd.DataFrame(data=dataVal);
skewValue = dataFrame.skew(axis=0)
print("DataFrame:")
print(dataFrame)
print("Skew:")
print(skewValue)
