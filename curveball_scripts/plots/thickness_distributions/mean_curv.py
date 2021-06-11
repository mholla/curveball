"""
Cortical thickness distribution profiles for positive and 
negative mean curvature with effect size for each individual
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import scipy.stats as stats

input_txt = 'subjects_Yale_TD.txt'
path = os.path.join(os.getcwd(),input_txt)
with open(path) as f: lines = f.read().splitlines()

t_gyr_H = []
t_sulc_H = []
d_H =[]

for line in lines:

    hemis = ['lh','rh']
        
    for hemi in hemis:
    
        H = '{h}.pial.H.asc'.format(h=hemi)
        t = '{h}.thickness.asc'.format(h=hemi)
        
        subjects_name = 'Yale_vtk'
        subjects_dir = os.path.join(os.getcwd(),subjects_name)
        subject = '{l}'.format(l=line)
        
        H = os.path.join(subjects_dir, subject, 'surf', H)
        t = os.path.join(subjects_dir, subject, 'surf', t)
        
        # read mean curvature
        with open(H,'r') as H_file:
            H_lines = H_file.readlines()
            
        H = np.zeros(len(H_lines))
            
        for i in range(len(H_lines)):
            H_data = H_lines[i].split()
            H[i] = H_data[4]
            
        # read cortical thickness   
        with open(t,'r') as t_file:
            t_lines = t_file.readlines()    
        
        t = np.zeros(len(t_lines))
        
        for i in range(len(t_lines)):
            t_data = t_lines[i].split()
            t[i] = t_data[4]
            
        for i in range(len(t)):
            if t[i] >= 5:
                t[i] = 0
                
        for i in range(len(t)):
            if t[i] <= 0.5:
                t[i] = 0
        
        H_gyr = np.zeros(len(H))
        t_gyr = np.zeros(len(t))
        H_sulc = np.zeros(len(H))
        t_sulc = np.zeros(len(t))
        
        for i in range(len(H)):
            if H[i] > 0:
                H_sulc[i] = H[i]
                t_sulc[i] = t[i]
                
        for i in range(len(H)):
            if H[i] < 0:
                H_gyr[i] = H[i]
                t_gyr[i] = t[i]
                
        for i in range(len(t)):
            if t_gyr[i] == 0:
                H_gyr[i] = 0
                
        for i in range(len(t)):
            if t_sulc[i] == 0:
                H_sulc[i] = 0
                    
        t_gyr = t_gyr[t_gyr != 0]
        t_sulc = t_sulc[t_sulc != 0]
        
        t_gyr_H = np.append(t_gyr_H, t_gyr)
        t_sulc_H = np.append(t_sulc_H, t_sulc)
        
    # length of samples
    n1 = len(t_gyr_H)
    n2 = len(t_sulc_H)
    
    # variance of the samples
    s1 = np.var(t_gyr_H, ddof=1)
    s2 = np.var(t_sulc_H, ddof=1)
    
    # pooled standard deviation
    s = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    
    # means of the samples
    u1 = np.mean(t_gyr_H)
    u2 = np.mean(t_sulc_H)
    
    # effect size
    d = (u1 - u2) / s
    d_H = np.append(d_H, d)
        
plt.figure()
ax = sns.kdeplot(t_sulc_H, color='#FDE725', shade=True, label='Positive H', bw_adjust=2, cut=0)
bx = sns.kdeplot(t_gyr_H, color='#31688E', shade=True, label='Negative H', bw_adjust=2, cut=0)
ax.set(xlim=(0.5, 5))
bx.set(xlim=(0.5, 5))
fname = '/Users/nagehan/Documents/Papers/1st_manuscript/high_res/mean_curv_dist.png'
plt.savefig(fname, dpi = 500)

#T-test
p = stats.ttest_ind(a=t_sulc_H,b=t_gyr_H,equal_var=False)
p_val = p[1]

plt.figure()
ax = sns.stripplot(data=[d_H], linewidth=1, color='white', edgecolor='black', size=7)
ax = sns.boxplot(data=[d_H], fliersize=0, linewidth=1.5, width = 0.25, color='lightgrey')
ax.set(ylim=(0, 1.2))
ax.tick_params(axis = "x", which = "both", bottom = False, top = False)
fname = '/Users/nagehan/Documents/Papers/1st_manuscript/high_res/mean_curv_effect.png'
plt.savefig(fname, dpi = 500)