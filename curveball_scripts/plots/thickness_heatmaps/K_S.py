"""
Variation of cortical thickness with respect to Gaussian curvature and sulcal depth 
for all individuals
t_map: cortical thickness matrix (per subject)
t_map_list: cortical thickness map of each individual subject
ind_map: total number of vertices map for each bounded region matrix (per subject)
ind_map_list: total number of vertices for each bounded region for all individuals
"""

import numpy as np
import os
from numpy import *
import numpy.ma as ma

input_txt = 'subjects_yale_TD.txt'
path = os.path.join(os.getcwd(),input_txt)
with open(path) as f: lines = f.read().splitlines()

t_map_list = {}
ind_map_list = {}
vertices = {}

for line in lines:
    
    K_all = []
    t_all = []
    S_all = []
    
    hemis = ['lh','rh']
        
    for hemi in hemis:
    
        subjects_name = 'Yale_vtk'
        subjects_dir = os.path.join(os.getcwd(),subjects_name)
        subject = '{l}'.format(l=line)
    
        S = '{h}.sulc.shrink_18.asc'.format(h=hemi)
        t = '{h}.thickness.asc'.format(h=hemi)
        K = '{h}.pial.K.asc'.format(h=hemi)
    
        S = os.path.join(subjects_dir, subject, 'surf', S)
        t = os.path.join(subjects_dir, subject, 'surf', t)
        K = os.path.join(subjects_dir, subject, 'surf', K)
    
        # read sulcal depth
        with open(S,'r') as S_file:
            S_lines = S_file.readlines()
            
        S = np.zeros(len(S_lines))
            
        for i in range(len(S_lines)):
            S_data = S_lines[i].split()
            S[i] = S_data[4]
            
        # read mean curvature
        with open(K,'r') as K_file:
            K_lines = K_file.readlines()
            
        K = np.zeros(len(K_lines))
            
        for i in range(len(K_lines)):
            K_data = K_lines[i].split()
            K[i] = K_data[4]
            
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
                S[i] = 0
                K[i] = 0
                
        for i in range(len(t)):
            if t[i] <= 0.5:
                t[i] = 0
                S[i] = 0
                K[i] = 0
                       
        for i in range(len(S)):
            if S[i] == 0:
                t[i] = 0
                K[i] = 0
                
        for i in range(len(K)):
            if K[i] == 0:
                t[i] = 0
                S[i] = 0
                
        K = K[K != 0]
        t = t[t != 0]   
        S = S[S != 0]
        
        K_all = np.append(K_all, K)
        t_all = np.append(t_all, t)
        S_all = np.append(S_all, S)
        # end of reading data
        
    # range of sulcal depth    
    div = 20
    s = np.around(np.linspace(min(S_all), max(S_all), div), decimals=1)
    
    k_s = np.zeros((len(s)-1, len(K_all)))
    t_s = np.zeros((len(s)-1, len(t_all)))
    
    for j in range(len(s) - 1):
        
        for i in range(len(S_all)):
            
            if S_all[i] >= s[j] and S_all[i] < s[j + 1]:
                k_s[j, i] = K_all[i]
                t_s[j, i] = t_all[i]
    
    # range of Gaussian curvature
    l = np.around(np.linspace(-0.05, 0.05, div), decimals=3) 
    
    t_map= np.zeros((len(s)-1, len(l)-1))
    ind_map = np.zeros((len(s)-1, len(l)-1))
    
    for k in range(len(s)-1):
        
        t_n = np.zeros((len(l)-1, len(t_all)))
    
        for j in range(len(l)-1):
    
            for i in range(len(K_all)):
            
                if k_s[k,i] >= l[j] and k_s[k,i] < l[j + 1]:
                    t_n[j, i] = t_s[k,i]
                
            d = t_n[j][t_n[j] != 0]        
            t_map[k,j] = np.mean(d)
            ind_map[k,j] = len(d)
    
    t_map = np.transpose(t_map)
    ind_map = np.transpose(ind_map)
    
    NaNs = isnan(t_map) # Replace nans with zeros in the t_map array
    t_map[NaNs] = 0
    
    t_map_list['t_map_{l}'.format(l=line)] = t_map
    ind_map_list['ind_map_{l}'.format(l=line)] = ind_map
    vertices['{l}'.format(l=line)] = len(K_all)
    
# reduce the subjects that has zero thickness mean before averaging over all subjects
subj_map = np.zeros([len(t_map),len(t_map)])

for i in range(len(subj_map)):
    subj_map[i] = 28

    
for i in range(len(s)-1):
    
    for j in range(len(s)-1):
        
        for line in lines:

            subjects_name = 'Yale_vtk'
            subjects_dir = os.path.join(os.getcwd(),subjects_name)
            subject = '{l}'.format(l=line)
            
            if t_map_list['t_map_{l}'.format(l=line)][i][j] == 0 or ind_map_list['ind_map_{l}'.format(l=line)][i][j] == 0:
                
                subj_map[i][j] = subj_map[i][j]-1

t_ave_map = np.zeros([len(t_map),len(t_map)])
ind_ave_map = np.zeros([len(t_map),len(t_map)])
                
for line in lines:
    
    subjects_name = 'Yale_vtk'
    subjects_dir = os.path.join(os.getcwd(),subjects_name)
    subject = '{l}'.format(l=line)
    
    t_ave_map = t_ave_map + t_map_list['t_map_{l}'.format(l=line)]
    ind_ave_map = ind_ave_map + ind_map_list['ind_map_{l}'.format(l=line)]
    
t_ave_map = t_ave_map / subj_map
ind_ave_map = ind_ave_map / subj_map

"""
Cortical thickness map with size of circles indicating total number of vertices
"""

def heatmap_circle(t_ave_map, ind_ave_map, s, l):
    
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.collections import PatchCollection
    
    # arrange size of the circles according to total # of vertex map
    N = len(t_ave_map)
    M = len(t_ave_map)
    
    size = np.zeros([M,N])
    
    for i in range(len(ind_ave_map)):
        for j in range(len(ind_ave_map)):
            if ind_ave_map[i,j] > 500:
                size[i,j] = 0.5
            elif ind_ave_map[i,j] > 100 and ind_ave_map[i,j] <= 500:
                size[i,j] = 0.4
            elif ind_ave_map[i,j] > 10 and ind_ave_map[i,j] <= 100:
                size[i,j] = 0.3
                
            else:
                size[i,j] = 0.2
            
    # reverse color map    
    color_map = plt.cm.get_cmap('viridis')
    rev_color_map = color_map.reversed()
    
    ylabels = l
    xlabels = s
    
    xlabels = xlabels[ : -1]
    
    x, y = np.meshgrid(np.arange(M), np.arange(N))
    
    fig, ax = plt.subplots()
    circles = [plt.Circle((j,i), radius=r) for r, j, i in zip(size.flat, x.flat, y.flat)]
    col = PatchCollection(circles, array=t_ave_map.flatten(), cmap=rev_color_map)
    ax.add_collection(col)
    ax.set_aspect(1)
    ax.set(xticks=np.arange(M-1)-0.5, yticks=np.arange(N+1)-0.5, xticklabels=xlabels, yticklabels=ylabels)
    ax.tick_params(axis='x', labelrotation = 45)
    plt.gca().invert_yaxis()
    
    fig.colorbar(col)
    plt.show()
    
    return


