"""
Total ICI(intrinsic curvature index) and FI(folding index) divided by surface area per individual 
for convex, concave, and saddle shaped points
"""

import matplotlib.pyplot as plt
import numpy as np
import os

input_txt = 'subjects_Yale_TD.txt'
path = os.path.join(os.getcwd(),input_txt)
with open(path) as f: lines = f.read().splitlines()

ICI_gyr_norm = []
ICI_sulc_norm = []
ICI_saddle_norm = []

mean_ICI_gyr = []
mean_ICI_sulc = []
mean_ICI_saddle = []

mean_FI_gyr = []
mean_FI_sulc = []
mean_FI_saddle = []

FI_gyr_norm = []
FI_sulc_norm = []
FI_saddle_norm = []

a_gyr_mean = []
a_sulc_mean = []
a_saddle_mean = []

for line in lines:
    
    ICI_gyr = []
    ICI_sulc = []
    ICI_saddle = []
    
    FI_gyr = []
    FI_sulc = []
    FI_saddle = []
    
    a_gyr = []
    a_sulc = []
    a_saddle = []
    
    hemis = ['lh','rh']
    
    for hemi in hemis:
  
        ICI_FI = '{h}.pial.ICI.FI.asc'.format(h=hemi)
    
        subjects_name = 'Yale_vtk'
        subjects_dir = os.path.join(os.getcwd(),subjects_name)
        subject = '{l}'.format(l=line)
        
        ICI_FI = os.path.join(subjects_dir, subject, 'surf', ICI_FI)
          
        # read ICI_FI_area data
        with open(ICI_FI,'r') as ICI_FI_file:
            ICI_FI_lines = ICI_FI_file.readlines()
            
        ICI_FI = np.zeros(len(ICI_FI_lines))
            
        ICI_FI_data = ICI_FI_lines[1].split()
        
        ICI_gyr = np.append(ICI_gyr, ICI_FI_data[0])
        ICI_sulc = np.append(ICI_sulc, ICI_FI_data[1])
        ICI_saddle = np.append(ICI_saddle, ICI_FI_data[2])
        
        FI_gyr = np.append(FI_gyr, ICI_FI_data[3])
        FI_sulc = np.append(FI_sulc, ICI_FI_data[4])
        FI_saddle = np.append(FI_saddle, ICI_FI_data[5])
        
        a_gyr = np.append(a_gyr, ICI_FI_data[9])
        a_sulc = np.append(a_sulc, ICI_FI_data[10])
        a_saddle = np.append(a_saddle, ICI_FI_data[11])
        
     
    # surface area
    a_gyr_mean = np.append(a_gyr_mean, np.mean(a_gyr.astype(np.float)))
    a_sulc_mean = np.append(a_sulc_mean, np.mean(a_sulc.astype(np.float)))
    a_saddle_mean = np.append(a_saddle_mean, np.mean(a_saddle.astype(np.float)))
    
    # normalized by area
    norm_ICI_gyr = np.mean(ICI_gyr.astype(np.float))/sum(a_gyr.astype(np.float)) 
    norm_FI_gyr = np.mean(FI_gyr.astype(np.float))/sum(a_gyr.astype(np.float)) 
    
    norm_ICI_sulc = np.mean(ICI_sulc.astype(np.float))/sum(a_sulc.astype(np.float)) 
    norm_FI_sulc = np.mean(FI_sulc.astype(np.float))/sum(a_sulc.astype(np.float)) 
    
    norm_ICI_saddle = np.mean(ICI_saddle.astype(np.float))/sum(a_saddle.astype(np.float)) 
    norm_FI_saddle = np.mean(FI_saddle.astype(np.float))/sum(a_saddle.astype(np.float)) 
    
    ICI_gyr_norm = np.append(ICI_gyr_norm, norm_ICI_gyr)
    FI_gyr_norm = np.append(FI_gyr_norm, norm_FI_gyr)
    
    ICI_sulc_norm = np.append(ICI_sulc_norm, norm_ICI_sulc)
    FI_sulc_norm = np.append(FI_sulc_norm, norm_FI_sulc)
    
    ICI_saddle_norm = np.append(ICI_saddle_norm, norm_ICI_saddle)
    FI_saddle_norm = np.append(FI_saddle_norm, norm_FI_saddle)
    
    # mean ICI, FI
    mean_ICI_gyr = np.append(mean_ICI_gyr, np.mean(ICI_gyr.astype(np.float)))
    mean_ICI_sulc = np.append(mean_ICI_sulc, np.mean(ICI_sulc.astype(np.float)))
    mean_ICI_saddle = np.append(mean_ICI_saddle, np.mean(ICI_saddle.astype(np.float)))
    
    mean_FI_gyr = np.append(mean_FI_gyr, np.mean(FI_gyr.astype(np.float)))
    mean_FI_sulc = np.append(mean_FI_sulc, np.mean(FI_sulc.astype(np.float)))
    mean_FI_saddle = np.append(mean_FI_saddle, np.mean(FI_saddle.astype(np.float)))

# mean norms
ICI_gyr_norm_mean = np.mean(ICI_gyr_norm)*1000
ICI_sulc_norm_mean = np.mean(ICI_sulc_norm)*1000
ICI_saddle_norm_mean = np.mean(ICI_saddle_norm)*1000

FI_gyr_norm_mean = np.mean(FI_gyr_norm)*1000
FI_sulc_norm_mean = np.mean(FI_sulc_norm)*1000
FI_saddle_norm_mean = np.mean(FI_saddle_norm)*1000

# std norms
ICI_gyr_norm_std = np.std(ICI_gyr_norm)*1000 #0.11
ICI_sulc_norm_std = np.std(ICI_sulc_norm)*1000 #0.28
ICI_saddle_norm_std = np.std(ICI_saddle_norm)*1000 #0.07

FI_gyr_norm_std = np.std(FI_gyr_norm)*1000 #0.07
FI_sulc_norm_std = np.std(FI_sulc_norm)*1000 #4.21
FI_saddle_norm_std = np.std(FI_saddle_norm)*1000 #1.11

# mean area
a_gyr_mean_mean = np.mean(a_gyr_mean)
a_sulc_mean_mean = np.mean(a_sulc_mean)
a_saddle_mean_mean = np.mean(a_saddle_mean)

# std area
a_gyr_mean_std = np.std(a_gyr_mean)
a_sulc_mean_std = np.std(a_sulc_mean)
a_saddle_mean_std = np.std(a_saddle_mean)

# barplot
data = [[ICI_gyr_norm_mean, FI_gyr_norm_mean, a_gyr_mean_mean/10000],
[ICI_sulc_norm_mean, FI_sulc_norm_mean, a_sulc_mean_mean/10000],
[abs(ICI_saddle_norm_mean), FI_saddle_norm_mean, a_saddle_mean_mean/10000]]

error = [[ICI_gyr_norm_std, FI_gyr_norm_std, a_gyr_mean_std/10000],
[ICI_sulc_norm_std, FI_sulc_norm_std, a_sulc_mean_std/10000],
[abs(ICI_saddle_norm_std), FI_saddle_norm_std, a_saddle_mean_std/10000]]

X = np.arange(3)
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(X + 0.00, data[0], color = 'grey', width = 0.25, yerr = error[0])
ax.bar(X + 0.25, data[1], color = 'darkgrey', width = 0.25, yerr = error[1])
ax.bar(X + 0.50, data[2], color = 'lightgrey', width = 0.25, yerr = error[2])
ax.legend(labels=['ICI_norm', 'FI_norm', 'Area'])
fig.show()
