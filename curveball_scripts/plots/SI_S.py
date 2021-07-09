"""
Variation of cortical thickness with respect to shape index and sulcal depth 
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
import heatmap_circle

input_txt = 'subjects_ABIDE_TD.txt'
path = os.path.join(os.getcwd(),input_txt)
with open(path) as f: lines = f.read().splitlines()

t_map_list = {}
ind_map_list = {}
vertices = {}

SI_all = []
t_all = []
S_all = []

for line in lines:
    
    SI_all = []
    t_all = []
    S_all = []
    
    hemis = ['lh','rh']
        
    for hemi in hemis:
    
        subjects_name = 'subjects_ABIDE_TD'
        subjects_dir = os.path.join(os.getcwd(),subjects_name)
        subject = '{l}'.format(l=line)
    
        S = '{h}.sulc.shrink.asc'.format(h=hemi)
        t = '{h}.thickness.asc'.format(h=hemi)
        SI = '{h}.pial.SI.asc'.format(h=hemi)
    
        S = os.path.join(subjects_dir, subject, 'surf', S)
        t = os.path.join(subjects_dir, subject, 'surf', t)
        SI = os.path.join(subjects_dir, subject, 'surf', SI)
    
        # reading sulcal depth
        with open(S,'r') as S_file:
            S_lines = S_file.readlines()
            
        S = np.zeros(len(S_lines))
            
        for i in range(len(S_lines)):
            S_data = S_lines[i].split()
            S[i] = S_data[4]
            
        # reading shape index
        with open(SI,'r') as SI_file:
            SI_lines = SI_file.readlines()
            
        SI = np.zeros(len(SI_lines))
            
        for i in range(len(SI_lines)):
            SI_data = SI_lines[i].split()
            SI[i] = SI_data[4]
            
        # reading cortical thickness
        with open(t,'r') as t_file:
            t_lines = t_file.readlines()
            
        t = np.zeros(len(t_lines))
            
        for i in range(len(t_lines)):
            t_data = t_lines[i].split()
            t[i] = t_data[4]
            
        for i in range(len(t)):
            if t[i] >= 5 or t[i] <= 0.5:
                t[i] = 0
                S[i] = 0
                SI[i] = 0            
                       
        for i in range(len(S)):
            if S[i] == 0:
                t[i] = 0
                SI[i] = 0
                
        for i in range(len(SI)):
            if SI[i] == 0:
                t[i] = 0
                S[i] = 0
                
        SI = SI[SI != 0]
        t = t[t != 0]   
        S = S[S != 0]
        
        SI_all = np.append(SI_all, SI)
        t_all = np.append(t_all, t)
        S_all = np.append(S_all, S)
        # end of reading data
    
    div = 20
    s = np.around(np.linspace(min(S_all), max(S_all), div), decimals=1)
    
    h_s = np.zeros((len(s)-1, len(SI_all)))
    t_s = np.zeros((len(s)-1, len(t_all)))
    
    for j in range(len(s)-1):
        
        for i in range(len(S)):
            
            if S[i] >= s[j] and S[i] < s[j + 1]:
                h_s[j, i] = SI[i]
                t_s[j, i] = t[i]
                
    l = np.around(np.linspace(-0.8, 0.8, div), decimals=2) # shape index range

    t_map= np.zeros((len(s)-1, len(l)-1))
    ind_map = np.zeros((len(s)-1, len(l)-1))
    
    for k in range(len(s)-1):
        
        t_n = np.zeros((len(l)-1, len(t)))
    
        for j in range(len(l)-1):
    
            for i in range(len(SI)):
            
                if h_s[k,i] >= l[j] and h_s[k,i] < l[j + 1]:
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
    vertices['{l}'.format(l=line)] = len(SI_all)
    
# reduce the subjects that has zero thickness mean before averaging over all subjects
subj_map = np.zeros([len(t_map),len(t_map)])

for i in range(len(subj_map)):
    subj_map[i] = len(lines)

    
for i in range(len(s)-1):
    
    for j in range(len(s)-1):
        
        for line in lines:

            subjects_name = 'subjects_ABIDE_TD'
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
Plot cortical thickness map; size of circles indicate total number of vertices within that range
"""

heatmap_circle.heatmap_circle(t_ave_map, ind_ave_map, s, l)
