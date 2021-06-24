#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code reproduces the actual human brain data cortical thickness ratio 
results of Wang et al 2020 (https://doi.org/....)

This code reads in the mean curvature (lh.pial.H.crv) and cortical thickness (lh. thickness) 
output files from ABIDE-YALE dataset (control group) obtained from the automatic neuroimaging 
pipeline Freesurfer (--recon-all) as an input to calculate the cortical thickness ratio of 
gyral and sulcal regions of the cortex depending on the sampling (coverage) ratio and mean 
cortical thickness of total gyral and sulcal regions identified by mean curvature (H).  

Create a folder and place all the input files (Yale_TD.txt and Yale_TD) into that folder.

The output ratio array is outputted as a .asc file to the user-defined folder for each subject. 

"""

def t_ratio(subjects_dir,subject,hemi):

    import numpy as np
    import os
    
    H = '{h}.pial.H.asc'.format(h=hemi)
    t = '{h}.thickness.asc'.format(h=hemi)
    
    H = os.path.join(subjects_dir, subject, 'surf', H)
    t = os.path.join(subjects_dir, subject, 'surf', t)
    
    with open(H,'r') as H_file:
        H_lines = H_file.readlines()
        
    h = np.zeros(len(H_lines))
        
    for i in range(len(H_lines)):
        H_data = H_lines[i].split()
        h[i] = H_data[4]
    
    with open(t,'r') as t_file:
        t_lines = t_file.readlines()
        
    t = np.zeros(len(t_lines))
        
    for i in range(len(t_lines)):
        t_data = t_lines[i].split()
        t[i] = t_data[4]
    
    gyral_sum = np.zeros(len(h))
    sulcal_sum = np.zeros(len(h))
        
    h = -h
    for i in range(len(h)):
        if h[i] > 0.0 and h[i] <= 0.5:
            gyral_sum[i] = h[i]
        
    for i in range(len(h)):
        if h[i] < 0.0 and h[i] >= -0.5:
            sulcal_sum[i] = h[i]
    
    t_gyral = np.zeros(len(t))
    t_sulcal = np.zeros(len(t))
    
    for i in range(len(t)):
        if gyral_sum[i] != 0:
            t_gyral[i] = t[i]
            
    for i in range(len(t)):
        if sulcal_sum[i] != 0:
            t_sulcal[i] = t[i]
    
    n_g = np.count_nonzero(t_gyral)
    n_s = np.count_nonzero(t_sulcal)
    
    coverage = np.array([0.01/100, 0.02/100, 0.04/100, 0.06/100, 0.08/100, 0.1/100, 0.2/100, 0.4/100, 0.6/100, 0.8/100, 1/100, 2/100, 4/100,
                         6/100, 8/100, 10/100, 20/100, 30/100, 40/100, 50/100, 60/100, 70/100, 80/100, 90/100, 1])

    N_g = n_g * coverage
    N_s = n_s * coverage

    # Cortical thickness ratio calculation for gyral and sulcal regions depending on sampling ratio (coverage)
    
    ratio = np.zeros(len(N_g))
    gyral_sorted = np.sort(gyral_sum)
    gyral_sorted_rev = gyral_sorted[::-1]
    sulcal_sorted = np.sort(sulcal_sum)
    
    for j in range(len(N_g)):
            
        t_g = np.zeros(len(t))
        t_s = np.zeros(len(t))
        
        gyral_reduced = gyral_sorted_rev[:int(N_g[j])]
        sulcal_reduced = sulcal_sorted[:int(N_s[j])]
        
        for k in range(len(gyral_sum)):
            if gyral_sum[k] >= min(gyral_reduced):
                t_g[k] = t_gyral[k]
        
        for m in range(len(sulcal_sum)):
            if sulcal_sum[m] <= max(sulcal_reduced):
                t_s[m] = t_sulcal[m]
        
        t_g = t_g[t_g != 0]
        t_s = t_s[t_s != 0]
               
        ratio[j] = np.mean(t_g)/np.mean(t_s)   

    array_name = os.path.join(subjects_dir, subject, 'surf', '{h}.thickness.ratio.asc'.format(h=hemi))
    np.savetxt(array_name, ratio, fmt='%10.6f', delimiter=' '' ')
        
    return 
    