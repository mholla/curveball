"""
Mean curvature distribution profile for all subjects
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import scipy.stats as stats
from matplotlib import colors
import statistics
from scipy.stats import skew
from scipy.stats import skewtest

input_txt = 'subjects_Yale_TD.txt'
path = os.path.join(os.getcwd(),input_txt)
with open(path) as f: lines = f.read().splitlines()

H_all = []

for line in lines:
    
    hemis = ['lh','rh']
        
    for hemi in hemis:
    
        H = '{h}.pial.H.asc'.format(h=hemi)
        
        subjects_name = 'Yale_vtk'
        subjects_dir = os.path.join(os.getcwd(),subjects_name)
        subject = '{l}'.format(l=line)
        
        H = os.path.join(subjects_dir, subject, 'surf', H)
            
       # reading mean curvature
        with open(H,'r') as H_file:
            H_lines = H_file.readlines()
            
        H = np.zeros(len(H_lines))
            
        for i in range(len(H_lines)):
            H_data = H_lines[i].split()
            H[i] = H_data[4]
        
        H[H < -1] = 0
        H[H > 1] = 0
        
        H = H[H != 0]
        
        H_all = np.append(H_all, H)
    
plt.figure()
ax=sns.kdeplot(H_all, color='#3E4A89', shade=True, bw_adjust=2)
ax.set(xlim=(-1, 1))
plt.show()

#Statistics
var = np.var(H_all)
mean = np.mean(H_all)
median = np.median(H_all)






