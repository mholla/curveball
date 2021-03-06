"""
Two iteration weighted average smoothing of each surface measure.

Parameters:
---------
    ndl: vertex neighbors from {h}.pial.neighbor.asc file
    nb: number of neighbors from {h}.pial.neighbor.asc file
    each surface measures from their corresponding text files (SI,H,K,k1,k2,thickness)
   
Returns:
------
   smoothed surface measures (SI.w2,H.w2,K.w2,k1.w2,k2.w2,thickness.w2) with two iterations saved as {h}.pial.{c}.w2.asc or
   {h}.{c}.w2.asc
"""

def smooth(subjects_dir,subject,x,y,z,hemi):
    
    import numpy as np
    import os

    curv = ['SI', 'H', 'K', 'k1', 'k2', 'thickness']

    for l in range(len(curv)):
        
        if curv[l] == 'thickness':
            curv_name = '{h}.{c}.asc'.format(c=curv[l], h=hemi) 
        else:
            curv_name = '{h}.pial.{c}.asc'.format(c=curv[l], h=hemi)
        
        input_name = os.path.join(subjects_dir, subject, 'surf', curv_name)
        input_data = np.zeros(len(x))
        
        with open(input_name,'r') as input_file:
            input_lines = input_file.readlines() 
            
        for i in range(len(input_lines)): 
            input_curv = input_lines[i].split()
            input_data[i] = float(input_curv[4])
        
        ################ Read the neighbor text file #####################
    
        input_ndl = '{h}.pial.neighbor.asc'.format(h=hemi)
        ndl_file = os.path.join(subjects_dir, subject, 'surf', input_ndl)
        ndl = np.loadtxt(ndl_file)
        nb = np.zeros(len(x)) 
           
        for i in range(len(x)):
            for j in range(len(ndl[0])):
                if ndl[i, j] == 0 and ndl[i, j+1] == 0:
                    nb[i] = j-1
                    break
            
        iteration = 2 # Iteration can be between 0-3
        strength  = 1 # Strength can be between 1-3
        
        for k in range(iteration):
        
            for i in range(len(ndl)): 
                
                total_dist   = 0
                total_weight = 0
                total_value = 0
        
                nd = ndl[i]
                le = int(nb[i]-2)
                
                if le <= 1: #corrupted vertices (one or two vertices can have zero area due to remeshing)
                    input_data[i] = input_data[i]
                    
                elif le > 1:
                
                    for j in range(1, le+1):
                        index = int(nd[j])
                        dist = np.sqrt((x[i] - x[index])**2 + (y[i] - y[index])**2 + (z[i] - z[index])**2)
                        total_dist = total_dist + dist
                        
                    for j in range(1, le+1):
                        index = int(nd[j])
                        dist = np.sqrt((x[i] - x[index])**2 + (y[i] - y[index])**2 + (z[i] - z[index])**2)
                        weight = 1.0 - (dist/total_dist)
                        total_weight = total_weight + weight
                        
                    for j in range(1, le+1):
                        
                        index = int(nd[j])
                        dist = np.sqrt((x[i] - x[index])**2 + (y[i] - y[index])**2 + (z[i] - z[index])**2)
                        weight = 1.0 - (dist/total_dist)
                        total_value = total_value + (input_data[index] * weight)/total_weight
                        
                    input_data[i] = (strength * total_value) + ((1-strength) * input_data[i])
         
        if curv[l] == 'thickness':
            curv_name = '{h}.{c}.w2.asc'.format(c=curv[l], h=hemi) # w2 means 2 iterations of smoothing
        else:
            curv_name = '{h}.pial.{c}.w2.asc'.format(c=curv[l], h=hemi) # w2 means 2 iterations of smoothing
        
        curv_name = os.path.join(subjects_dir, subject, 'surf', curv_name)
    
        indices = np.array(range(len(input_data)))
        columns = np.column_stack([x, y, z, input_data])
    
        np.savetxt(curv_name, indices, fmt='%03d', delimiter=' '' ') 
    
        with open(curv_name,'r') as f:
            lines = f.read().splitlines()
            with open(curv_name, 'w') as f: 
                for i in range(len(columns)):
                    f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i,0])  + ' ' + '%10.6f' % (columns[i,1])
                    + ' ' + '%10.6f' % (columns[i,2]) + ' ' + '%10.6f' % (columns[i,3])])+ '\n')  
    
    return 
