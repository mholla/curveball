"""
By: Cameron on 1/10/2024
Parameters:
---------
    H: Mean curvature at each vertex read from {h}.pial.H.asc file
    K: Gaussian curvature at each vertex read from {h}.pial.K.asc file

Returns:
-------
   k1: 1st principal curvature at each vertex saved to {h}.pial.k1.asc file
   k2: 2nd principal curvature at each vertex saved to {h}.pial.k2.asc file
   SI: Shape index at each vertex saved to {h}.pial.SI.asc file
   CVD: Curvedness at each vertex saved to {h}.pial.cvd.asc file
"""

def k1_k2_SI_CVD(x, y, z, subjects_dir, subject, hemi):
    import numpy as np
    import os

    H = '{h}.pial.H.asc'.format(h=hemi)
    K = '{h}.pial.K.asc'.format(h=hemi)
    
    # Path is already correct: subjects_dir is the full path
    H = os.path.join(subjects_dir, 'surf', H)
    K = os.path.join(subjects_dir, 'surf', K)
    
    # checks if file exists
    try:
        with open(H, 'r') as H_file:
            H_lines = H_file.readlines()
    except FileNotFoundError:
        print(f"Error: Mean curvature file {H} not found for subject {subject}, hemi {hemi}")
        return
    
    h = np.zeros(len(H_lines))
        
    for i in range(len(H_lines)):
        H_data = H_lines[i].split()
        h[i] = float(H_data[4]) # grabs 5th column which is mean curvature
        
    try:
        with open(K, 'r') as K_file:
            K_lines = K_file.readlines()
    except FileNotFoundError:
        print(f"Error: Gaussian curvature file {K} not found for subject {subject}, hemi {hemi}")
        return
        
    k = np.zeros(len(K_lines))
        
    for i in range(len(K_lines)):
        K_data = K_lines[i].split()
        k[i] = float(K_data[4])
              
    k1 = np.zeros(len(h))
    k2 = np.zeros(len(h))
    SI = np.zeros(len(h))
              
    for i in range(len(h)):
        # Calculate principal curvatures            
        sqrt_term = h[i] ** 2 - k[i]
        if sqrt_term < 0: # makes sure no imaginary numbers occur
            sqrt_term = 0
        try: 
            k1[i] = h[i] + np.sqrt(sqrt_term)
            k2[i] = h[i] - np.sqrt(sqrt_term)
        except Warning: 
            print(f'Warning: Calculating principal curvatures at vertex {i}, H={h[i]}, K={k[i]} for subject {subject}, hemi {hemi}')
        
        # Calculate shape index
        denom_term = k1[i] - k2[i]
        if denom_term == 0: 
            SI[i] = 0
        else: 
            try: 
                SI[i] = (2/np.pi) * np.arctan2((k1[i] + k2[i]), denom_term) # chnaged to arctan2 to consider quadrants
            except Warning: 
                print(f'Warning: Calculating shape index from principal curvatures k1={k1[i]}, k2={k2[i]} for subject {subject}, hemi {hemi}')
                
    k1_name = '{h}.pial.k1.asc'.format(h=hemi)
    k2_name = '{h}.pial.k2.asc'.format(h=hemi)
    SI_name = '{h}.pial.SI.asc'.format(h=hemi)
    
    k1_name = os.path.join(subjects_dir, 'surf', k1_name)
    k2_name = os.path.join(subjects_dir, 'surf', k2_name)
    SI_name = os.path.join(subjects_dir, 'surf', SI_name)
    
    # Save k1 to .asc file
    indices = np.array(range(len(k1)))
    columns = np.column_stack([x, y, z, k1])
    
    np.savetxt(k1_name, indices, fmt='%03d', delimiter=' ') 
    
    with open(k1_name, 'r') as f:
        lines = f.read().splitlines()
    with open(k1_name, 'w') as f: 
        for i in range(len(columns)):
            f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i, 0]) + ' ' + '%10.6f' % (columns[i, 1])
                             + ' ' + '%10.6f' % (columns[i, 2]) + ' ' + '%10.6f' % (columns[i, 3])]) + '\n') 
    
    # Save k2 to .asc file
    indices = np.array(range(len(k2)))
    columns = np.column_stack([x, y, z, k2])
    
    np.savetxt(k2_name, indices, fmt='%03d', delimiter=' ') 
    
    with open(k2_name, 'r') as f:
        lines = f.read().splitlines()
    with open(k2_name, 'w') as f: 
        for i in range(len(columns)):
            f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i, 0]) + ' ' + '%10.6f' % (columns[i, 1])
                             + ' ' + '%10.6f' % (columns[i, 2]) + ' ' + '%10.6f' % (columns[i, 3])]) + '\n') 
    
    # Save SI file
    indices = np.array(range(len(SI)))
    columns = np.column_stack([x, y, z, SI])
    
    np.savetxt(SI_name, indices, fmt='%03d', delimiter=' ') 
    
    with open(SI_name, 'r') as f:
        lines = f.read().splitlines()
    with open(SI_name, 'w') as f: 
        for i in range(len(columns)):
            f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i, 0]) + ' ' + '%10.6f' % (columns[i, 1])
                             + ' ' + '%10.6f' % (columns[i, 2]) + ' ' + '%10.6f' % (columns[i, 3])]) + '\n') 
    
    # Calculate curvedness (cvd)
    cvd = np.sqrt((k1 ** 2 + k2 ** 2) / 2)

    # Save cvd to .asc file
    cvd_name = '{h}.pial.cvd.asc'.format(h=hemi)
    cvd_name = os.path.join(subjects_dir, 'surf', cvd_name)

    indices = np.array(range(len(cvd)))
    columns = np.column_stack([x, y, z, cvd])

    np.savetxt(cvd_name, indices, fmt='%03d', delimiter=' ')

    with open(cvd_name, 'r') as f:
        lines = f.read().splitlines()
    with open(cvd_name, 'w') as f:
        for i in range(len(columns)):
            f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i, 0]) + ' ' + '%10.6f' % (columns[i, 1])
                           + ' ' + '%10.6f' % (columns[i, 2]) + ' ' + '%10.6f' % (columns[i, 3])]) + '\n')

    return