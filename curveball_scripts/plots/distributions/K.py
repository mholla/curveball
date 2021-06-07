"""
Gaussian curvature distribution profile for all subjects
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

input_txt = 'subjects_Yale_TD.txt'
path = os.path.join(os.getcwd(),input_txt)
with open(path) as f: lines = f.read().splitlines()

K_all = []

for line in lines:
    
    hemis = ['lh','rh']
        
    for hemi in hemis:
    
        K = 'lh.pial.K.asc'
        
        subjects_name = 'Yale_vtk'
        subjects_dir = os.path.join(os.getcwd(),subjects_name)
        subject = '{l}'.format(l=line)
        
        K = os.path.join(subjects_dir, subject, 'surf', K)
            
       # read Gaussian curvature
        with open(K,'r') as K_file:
            K_lines = K_file.readlines()
            
        K = np.zeros(len(K_lines))
            
        for i in range(len(K_lines)):
            K_data = K_lines[i].split()
            K[i] = K_data[4]
        
        K[K < -0.1] = 0
        K[K > 0.1] = 0
        
        K = K[K != 0]
        K_all = np.append(K_all, K)
    
plt.figure()
ax = sns.kdeplot(K_all, color='#3E4A89', shade=True, bw_adjust=2)
ax.set(xlim=(-0.1, 0.1))
plt.show()

#Statistics
var = np.var(K_all)
mean = np.mean(K_all)
median = np.median(K_all)

