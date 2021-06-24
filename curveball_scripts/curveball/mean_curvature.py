"""
inputs: 
   vertex neighbors(ndl)
   max number of neighbor(nb)
outputs: 
   mean curvature (H) at each vertex
"""

def mean_curvature(x,y,z,subjects_dir,subject,hemi):
    
    import numpy as np
    import math
    import os
    
    ################ Read the neighbor text file #####################

    input_ndl = '{h}.pial.neighbor.asc'.format(h=hemi)
    
    ndl_file = os.path.join(subjects_dir, subject, 'surf', input_ndl)
    ndl = np.loadtxt(ndl_file)
    
    nb = np.zeros(len(ndl)) # max number of neighbor for each vertex
       
    for i in range(len(ndl)):
        for j in range(3,len(ndl[0])):
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
    
    ###################################################################
    
    h_tri = np.zeros((len(x), max_nb))

    for h in range(len(x)):
        
        if h in skip_vertex: # skip the bad vertices with bad connectivity
            continue
        
        le = int(nb[h] + 1)
        k = np.array(ndl[h, :le])
        j=1
        
        for i in k:
            
            if j==le-2:
                break
            
            p2 = np.array([x[int(h)], y[int(h)], z[int(h)]]) #Vertex in consideration
            
            ind1 = int(k[j])
            ind2 = int(k[j+1])
            ind3 = int(k[j+2])
            
            p1 = np.array([x[ind1], y[ind1], z[ind1]])
            p3 = np.array([x[ind2], y[ind2], z[ind2]])
            p4 = np.array([x[ind3], y[ind3], z[ind3]])
                        
            q1 = np.subtract(p2,p1)
            q2 = np.subtract(p3,p2)
            q3 = np.subtract(p4,p3)
            
            q1_x_q2 = np.cross(q1,q2)
            q2_x_q3 = np.cross(q2,q3)
            
            n1 = q1_x_q2/np.sqrt(np.dot(q1_x_q2,q1_x_q2))
            n2 = q2_x_q3/np.sqrt(np.dot(q2_x_q3,q2_x_q3))
            n2 = -n2
            
            u1 = n2
            u3 = q2/(np.sqrt(np.dot(q2,q2)))
            u2 = np.cross(u3,u1)
            
            cost = np.dot(n1, u1)
            sint = np.dot(n1, u2)
            
            theta = -math.atan2(sint,cost)
            
            edge = np.sqrt((x[int(h)] - x[ind2])**2 + (y[int(h)] - y[ind2])**2 + (z[int(h)] - z[ind2])**2)
            
            h_tri[h, j] = theta*edge
            
            j = j + 1
            

    H_sum = np.zeros(len(x))

    for i in range(len(x)):

        H_sum[i] = sum(h_tri[i,:])   

    """
    Total area of all the triangles meeting at each vertex is needed. Mean curv is normalized by that.
    The area was calculated (and saved) in the Gaussian curv code and the file is called here.

    """  
    #Read the area file
    
    a_name = '{h}.pial.area.asc'.format(h=hemi)
    
    a_name = os.path.join(subjects_dir, subject, 'surf', a_name)
    a_sum = np.zeros(len(H_sum))
    
    with open(a_name,'r') as coord_file:
        coord_lines = coord_file.readlines() 
        
    for i in range(len(coord_lines)): 
    
        coord_data = coord_lines[i].split()
        a_sum[i] = float(coord_data[4])

    H = H_sum/4/(a_sum/3) # This is the final mean curvature

    H_name = '{h}.pial.H.asc'.format(h=hemi)
    H_name = os.path.join(subjects_dir, subject, 'surf', H_name)

    indices = np.array(range(len(H)))
    columns = np.column_stack([x, y, z, H])
    
    np.savetxt(H_name, indices, fmt='%03d', delimiter=' '' ') 
    
    with open(H_name,'r') as f:
        lines = f.read().splitlines()
    with open(H_name, 'w') as f: 
        for i in range(len(columns)):
            f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i,0])  + ' ' + '%10.6f' % (columns[i,1])
            + ' ' + '%10.6f' % (columns[i,2]) + ' ' + '%10.6f' % (columns[i,3])])+ '\n')  

    return 

     
