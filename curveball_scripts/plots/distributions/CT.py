"""
Cortical thickness distribution profile for all subjects
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

t_all = []

for line in lines:
    
    hemis = ['lh','rh']
    
    for hemi in hemis:
    
        t = 'lh.thickness.asc'
        
        subjects_name = 'Yale_vtk'
        subjects_dir = os.path.join(os.getcwd(),subjects_name)
        subject = '{l}'.format(l=line)
        
        t = os.path.join(subjects_dir, subject, 'surf', t)
            
        # reading cortical thickness   
        with open(t,'r') as t_file:
            t_lines = t_file.readlines()    
        
        t = np.zeros(len(t_lines))
        
        for i in range(len(t_lines)):
            t_data = t_lines[i].split()
            t[i] = t_data[4]
            
        t[t < 0.5] = 0
        t[t > 5] = 0
        t = t[t != 0]
    
        t_all = np.append(t_all, t)

plt.figure()
sns.kdeplot(t_all, color='#3E4A89', shade=True, bw_adjust=3, label='Cortical thickness')
plt.legend(loc='best', prop={'size': 12})
fname = '/Users/nagehan/Documents/Papers/1st_manuscript/high_res/ct.png'
plt.savefig(fname, dpi = 500)

#Statistics
var = statistics.variance(t_all)
var = np.var(t_all)
mean = np.mean(t_all)
skew = skew(t_all)
std = np.std(t_all)
mode = statistics.mode(t_all)
median = statistics.median(t_all)
