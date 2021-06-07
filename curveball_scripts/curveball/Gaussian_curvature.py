"""
inputs: 
   vertex neighbors(ndl)
   max number of neighbor(nb)
outputs: 
   surface area associated with each vertex
   Gaussian curvature (K) at each vertex
"""

def Gaussian_curvature(x,y,z,subjects_dir,subject):
    
    import numpy as np
    import os
    
    hemis = ['lh','rh']
    
    for hemi in hemis:
    
        # Read the neighbor text file
        
        input_ndl = '{h}.pial.neighbor.asc'.format(h=hemi)
        ndl_file = os.path.join(subjects_dir, subject, 'surf', input_ndl)
        ndl = np.loadtxt(ndl_file)
        
        nb = np.zeros(len(x)) # max number of neighbor for each vertex
           
        for i in range(len(x)):
            for j in range(3, len(ndl[0])):
                if ndl[i, 2] == ndl[i, j]:
                    nb[i] = j
                    break
                
        max_nb = int(max(nb))
        
        # Check for bad vertices due to bad connectivity of the mesh at that vertex
        skip_vertex = np.array([])
        
        for i in range(len(ndl)):
        
            le = int(nb[i]-2)
            
            if ndl[i, le+1] != ndl[i, 1] or nb[i] <= 3:
                skip_vertex = np.append(skip_vertex, i) 
        
        # Euclidean distance of each neighbor from the main vertex
        
        dist_from_vertex = np.zeros((len(x), max_nb))
        
        for i in range(len(ndl)): 
          
            nd = ndl[i]
            le = int(nb[i]-2)
            dist_from_vertex[i,0] = i
            
            for j in range(1, le+1):
                
                index = int(nd[j])
                dist_from_vertex[i,j] = np.sqrt((x[i] - x[index])**2 + (y[i] - y[index])**2 + (z[i] - z[index])**2)
            
            dist_from_vertex[i,j+1] = dist_from_vertex[i,1]
        
        ############## Sum of internal angles #################
        
        theta = np.zeros((len(x), max_nb)) # Internal angles for each triangle connecting at a specific vertex
        param = np.zeros((len(x), max_nb)) # Semi-parameter of each triangle
        parea = np.zeros((len(x), max_nb)) # Area of each triangle, patch area
            
        for h in range(len(x)): 
            
            if h in skip_vertex: 
                continue
            
            nd = ndl[h]
            le = int(nb[h]-2)
            
            for j in range(1,le+1):
                
                k = dist_from_vertex[h, j]
                l = dist_from_vertex[h, j + 1]
                
                ind1 = int(nd[j])
                ind2 = int(nd[j + 1])
                
                m = np.sqrt((x[ind1] - x[ind2])**2 + (y[ind1] - y[ind2])**2 + (z[ind1] - z[ind2])**2)
                
                theta[h,j-1] = np.arccos((k**2 + l**2 - m**2)/(2*k*l))
                param[h,j-1] = (k + l + m)/2
                parea[h,j-1] = np.sqrt(param[h,j-1]*(param[h,j-1]-l)*(param[h,j-1]-k)*(param[h,j-1]-m))
        
        
        theta_sum = np.zeros(len(x)) # Sum of internal angles of each triangle meeting at each vertex
        K_gb = np.zeros(len(x)) # Sum of angle excess or defect
        a_sum = np.zeros(len(x)) #Sum of area of triangles meeting at each vertex
        
        for i in range(len(x)):
            
            theta_sum[i] = sum(theta[i,:])
            a_sum[i] = sum(parea[i,:])
            K_gb[i] = 2*np.pi - theta_sum[i]
            
        # Check if there are any zero areas due to mesh and/or connectivity and set a low but not zero value
        
        for i in range(len(a_sum)):
            if a_sum[i] == 0:
                a_sum[i] = 0.001
        
        K = K_gb/(a_sum/3) # This is the final Gaussian curvature
        
        for i in range(len(K)):
            if K[i] > 1000: # a very large number due to bad vertices with bad connectivity
                K[i] = 0
            
        # Save Gaussian curvature and area data - In Freesurfer curvature file format
        
        K_name = '{h}.pial.K.asc'.format(h=hemi)
        a_name = '{h}.pial.area.asc'.format(h=hemi)
        
        K_name = os.path.join(subjects_dir, subject, 'surf', K_name)
    
        indices = np.array(range(len(K)))
        columns = np.column_stack([x, y, z, K])
    
        np.savetxt(K_name, indices, fmt='%03d', delimiter=' '' ') 
    
        with open(K_name,'r') as f:
            lines = f.read().splitlines()
        with open(K_name, 'w') as f: 
            for i in range(len(columns)):
                f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i,0])  + ' ' + '%10.6f' % (columns[i,1])
                + ' ' + '%10.6f' % (columns[i,2]) + ' ' + '%10.6f' % (columns[i,3])])+ '\n')  
    
        a_name = os.path.join(subjects_dir, subject, 'surf', a_name)
    
        indices = np.array(range(len(a_sum)))
        columns = np.column_stack([x, y, z, a_sum])
        
        np.savetxt(a_name, indices, fmt='%03d', delimiter=' '' ') 
        
        with open(a_name,'r') as f:
            lines = f.read().splitlines()
        with open(a_name, 'w') as f: 
            for i in range(len(columns)):
                f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i,0])  + ' ' + '%10.6f' % (columns[i,1])
                + ' ' + '%10.6f' % (columns[i,2]) + ' ' + '%10.6f' % (columns[i,3])])+ '\n')  
        
    return 








                        