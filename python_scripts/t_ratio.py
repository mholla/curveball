"""
Cortical thickness ratio (t_gyral/t_sulcal) calculated at various coverage ratios using mean curvature.
For more information, the users are referred to Wang et al, 2021 (https://link.springer.com/article/10.1007/s10237-020-01400-w)

Parameters:
---------
    Surface measures: mean curvature from {h}.pial.H.asc and cortical thickness from {h}.thickness.asc files
Returns:
-------
    Cortical thickness ratio: {h}.thickness.ratio.asc
"""

def t_ratio(subjects_dir, subject, hemi):
    import numpy as np
    import os
    
    # Define input file names
    H = '{h}.pial.H.asc'.format(h=hemi)
    t = '{h}.thickness.asc'.format(h=hemi)
    
    # Fixed paths: Remove 'subject' since subjects_dir is the full path
    H = os.path.join(subjects_dir, 'surf', H)
    t = os.path.join(subjects_dir, 'surf', t)
    
    # Reading mean curvature
    try:
        with open(H, 'r') as H_file:
            H_lines = H_file.readlines()
    except FileNotFoundError:
        print(f"Error: Mean curvature file {H} not found for subject {subject}, hemi {hemi}")
        return
    
    h = np.zeros(len(H_lines))
    for i in range(len(H_lines)):
        H_data = H_lines[i].split()
        h[i] = float(H_data[4])
    
    # Reading cortical thickness
    try:
        with open(t, 'r') as t_file:
            t_lines = t_file.readlines()
    except FileNotFoundError:
        print(f"Error: Cortical thickness file {t} not found for subject {subject}, hemi {hemi}")
        return
    
    t = np.zeros(len(t_lines))
    for i in range(len(t_lines)):
        t_data = t_lines[i].split()
        t[i] = float(t_data[4])
    
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
    gyral_sorted_rev = gyral_sorted[::-1] # descending order
    sulcal_sorted = np.sort(sulcal_sum) # ascending order
    
    for j in range(len(N_g)):
        t_g = np.zeros(len(t))
        t_s = np.zeros(len(t))
        
        gyral_reduced = gyral_sorted_rev[:int(N_g[j])] # slices based on N_g[i] (number of elements taken from vector)
        sulcal_reduced = sulcal_sorted[:int(N_s[j])]
        
        for k in range(len(gyral_sum)):
            if gyral_sum[k] >= min(gyral_reduced):
                t_g[k] = t_gyral[k]
        
        for m in range(len(sulcal_sum)):
            if sulcal_sum[m] <= max(sulcal_reduced):
                t_s[m] = t_sulcal[m]
        
        t_g = t_g[t_g != 0]
        t_s = t_s[t_s != 0]
               
        # Handle empty arrays to prevent errors in np.mean
        mean_t_g = np.mean(t_g) if len(t_g) > 0 else 0
        mean_t_s = np.mean(t_s) if len(t_s) > 0 else 0
        
        # Avoid division by zero
        ratio[j] = mean_t_g / mean_t_s if mean_t_s != 0 else 0

    # Fixed path
    array_name = os.path.join(subjects_dir, 'surf', '{h}.thickness.ratio.asc'.format(h=hemi))
    np.savetxt(array_name, ratio, fmt='%10.6f', delimiter=' ')
        
    return