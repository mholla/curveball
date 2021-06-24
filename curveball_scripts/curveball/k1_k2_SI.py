"""
inputs: 
   mean curvature at each vertex
   Gaussian curvature at ecah vertex
outputs: 
   principal curvatures k1, k2
   shape index (SI)
"""

def k1_k2_SI(x,y,z,subjects_dir,subject,hemi):
    
    import numpy as np
    import os

    H = '{h}.pial.H.asc'.format(h=hemi)
    K = '{h}.pial.K.asc'.format(h=hemi)
    
    H = os.path.join(subjects_dir, subject, 'surf', H)
    K = os.path.join(subjects_dir, subject, 'surf', K)
    
    with open(H,'r') as H_file:
        H_lines = H_file.readlines()
        
    h = np.zeros(len(H_lines))
        
    for i in range(len(H_lines)):
        H_data = H_lines[i].split()
        h[i] = H_data[4]
        
    with open(K,'r') as K_file:
        K_lines = K_file.readlines()
        
    k = np.zeros(len(K_lines))
        
    for i in range(len(K_lines)):
        K_data = K_lines[i].split()
        k[i] = K_data[4]
              
    k1 = np.zeros(len(h))
    k2 = np.zeros(len(h))
    SI = np.zeros(len(h))
              
    for i in range(len(h)):
        
        # calculate principal curvatures            
        sqrt_term = h[i] ** 2 - k[i]
        
        if sqrt_term < 0:
            sqrt_term = 0
        try: 
            k1[i] = h[i] + np.sqrt(sqrt_term)
            k2[i] = h[i] - np.sqrt(sqrt_term)
        except Warning: 
            print('Warning: calculating principal curvatures from', i, h[i], k[i])
        
        # calculate shape index
        denom_term = k2[i] - k1[i]
        
        if denom_term == 0: 
            SI[i] = 0
        else: 
            try: 
                SI[i] = 2 * np.arctan((k2[i] + k1[i])/denom_term)/np.pi
            except Warning: 
                print ('Warning: calculating shape index from principal curvatures', k1[i], k2[i])
                
    k1_name = '{h}.pial.k1.asc'.format(h=hemi)
    k2_name = '{h}.pial.k2.asc'.format(h=hemi)
    SI_name = '{h}.pial.SI.asc'.format(h=hemi)
    
    k1_name = os.path.join(subjects_dir, subject, 'surf', k1_name)
    k2_name = os.path.join(subjects_dir, subject, 'surf', k2_name)
    SI_name = os.path.join(subjects_dir, subject, 'surf', SI_name)
    
    # save k1 to .asc file
    indices = np.array(range(len(k1)))
    columns = np.column_stack([x, y, z, k1])
    
    np.savetxt(k1_name, indices, fmt='%03d', delimiter=' '' ') 
    
    with open(k1_name,'r') as f:
        lines = f.read().splitlines()
    with open(k1_name, 'w') as f: 
        for i in range(len(columns)):
            f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i,0])  + ' ' + '%10.6f' % (columns[i,1])
            + ' ' + '%10.6f' % (columns[i,2]) + ' ' + '%10.6f' % (columns[i,3])])+ '\n') 
        
    # save k2 to .asc file
    indices = np.array(range(len(k2)))
    columns = np.column_stack([x, y, z, k2])
    
    np.savetxt(k2_name, indices, fmt='%03d', delimiter=' '' ') 
    
    with open(k2_name,'r') as f:
        lines = f.read().splitlines()
    with open(k2_name, 'w') as f: 
        for i in range(len(columns)):
            f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i,0])  + ' ' + '%10.6f' % (columns[i,1])
            + ' ' + '%10.6f' % (columns[i,2]) + ' ' + '%10.6f' % (columns[i,3])])+ '\n') 
    
    # save SI to .asc file
    indices = np.array(range(len(SI)))
    columns = np.column_stack([x, y, z, SI])
    
    np.savetxt(SI_name, indices, fmt='%03d', delimiter=' '' ') 
    
    with open(SI_name,'r') as f:
        lines = f.read().splitlines()
    with open(SI_name, 'w') as f: 
        for i in range(len(columns)):
            f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i,0])  + ' ' + '%10.6f' % (columns[i,1])
            + ' ' + '%10.6f' % (columns[i,2]) + ' ' + '%10.6f' % (columns[i,3])])+ '\n') 
    
    return 



