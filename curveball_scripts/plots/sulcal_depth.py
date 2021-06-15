"""
Cortical thickness distribution profiles for interior and exterior vertices, 
below and above the mid cortical surface with effect size per individual.
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

input_txt = 'subjects_Yale_TD.txt'
path = os.path.join(os.getcwd(),input_txt)
with open(path) as f: lines = f.read().splitlines()

t_sulc_S = []
t_gyr_S = []

d_S = []

for line in lines:
    
    hemis = ['lh','rh']
    
    for hemi in hemis:
        
        S = '{h}.sulc.shrink.asc'.format(h=hemi)
        t = '{h}.thickness.asc'.format(h=hemi)
        
        subjects_name = 'Yale_vtk'
        subjects_dir = os.path.join(os.getcwd(),subjects_name)
        subject = '{l}'.format(l=line)
        
        S = os.path.join(subjects_dir, subject, 'surf', S)
        t = os.path.join(subjects_dir, subject, 'surf', t)
        
        # read sulcal depth
        with open(S,'r') as S_file:
            S_lines = S_file.readlines()
            
        S = np.zeros(len(S_lines))
            
        for i in range(len(S_lines)):
            S_data = S_lines[i].split()
            S[i] = S_data[4]
            
        # read cortical thickness
        with open(t,'r') as t_file:
            t_lines = t_file.readlines()
            
        t = np.zeros(len(t_lines))
            
        for i in range(len(t_lines)):
            t_data = t_lines[i].split()
            t[i] = t_data[4]
            
        for i in range(len(t)):
            if t[i] > 5:
                t[i] = 0
                
        for i in range(len(t)):
            if t[i] < 0.5:
                t[i] = 0
                
        for i in range(len(t)):
            if t[i] == 0:
                S[i] = 0
                
        t = t[t != 0]
        S = S[S != 0]
                
        # Sulcal depth divided into t_sulc and t_gyral 
        S_gyr = np.zeros(len(S))
        S_sulc = np.zeros(len(S))
        
        t_gyr = np.zeros(len(t))
        t_sulc = np.zeros(len(t))
        
        for i in range(len(S)):
            if S[i] < 0:
                S_gyr[i] = S[i]
                t_gyr[i] = t[i]
                
        for i in range(len(S)):
            if S[i] > 0:
                S_sulc[i] = S[i]
                t_sulc[i] = t[i]
                
        t_gyr = t_gyr[t_gyr != 0]
        t_sulc = t_sulc[t_sulc != 0]
        
        S_gyr = S_gyr[S_gyr != 0]
        S_sulc = S_sulc[S_sulc != 0]
                
        t_gyr_S = np.append(t_gyr_S, t_gyr)
        t_sulc_S = np.append(t_sulc_S, t_sulc)

    # sample sizes
    n1 = len(t_gyr_S)
    n2 = len(t_sulc_S)
    
    #  variance of the samples
    s1 = np.var(t_gyr, ddof=1)
    s2 = np.var(t_sulc, ddof=1)
    
    # pooled standard deviation
    s = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    
    # means of the samples
    u1 = np.mean(t_gyr)
    u2 = np.mean(t_sulc)
    
    # effect size
    d = (u2 - u1) / s
    d_S = np.append(d_S, d)
                       
plt.figure()
ax = sns.kdeplot(t_gyr_S, color='#FDE725', shade=True, label = 'S>0', bw_adjust=3)
bx = sns.kdeplot(t_sulc_S, color='#31688E', shade=True, label = 'S<0', bw_adjust= 3)
plt.legend(loc='best', prop={'size': 14})
ax.set(xlim=(0.5, 5))
bx.set(xlim=(0.5, 5))
fname = '/Users/nagehan/Documents/Papers/1st_manuscript/high_res/s_depth_dist.png'
plt.savefig(fname, dpi = 500)

#Box plot
plt.figure()
cx = sns.stripplot(data=[d_S], linewidth=1, color='white', edgecolor='black', size=7)
cx = sns.boxplot(data=[d_S], fliersize=0, linewidth=1.5, width = 0.3, color='lightgrey')
cx.set(ylim=(0, 1.2))
fname = '/Users/nagehan/Documents/Papers/1st_manuscript/high_res/s_depth_effect.png'
plt.savefig(fname, dpi = 500)


