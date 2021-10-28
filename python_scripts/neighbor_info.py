"""
Find the neighbors of each vertex of the surface mesh and outputs to a text file. 

Parameters:
---------
     a,b,c,x,y,z: Outputs from the coord_nodes.py file
     subjects_dir, subject, hemi: These are defined in the curveball.py file
     
Returns:
-------
    ndl: vertex neighbor information stored in a circular order (CW or CCW) for each vertex.
         Row length is equal to the total number of vertices.
         Column length is arbitrary (here it is assigned as 35) but must be higher
         than the maximum number of neighbor that any vertex might have.
         The data is saved to {h}.pial.neighbor.asc file for each hemisphere

    nb: total number of neighbor for each vertex

    max_nb: Maximum number of neighbors that a vertex has in the mesh 
"""

def neighbor_info(a,b,c,x,y,z,subjects_dir,subject,hemi):
    
    import numpy as np
    import os
    
    # Set an arbitrarily large value for max number of neighbor that a vertex can have
    max_nb = 35

    ####### Vertex number ##########################
    
    ndl = np.zeros((len(x), max_nb)) 
    for i in range(len(x)):
        ndl[i,0] = i

    ############ First two neighbors ######################

    j = int(0)

    for h in range(len(x)):
        
        for i in range(len(a)):
            
            if  a[i] == h:
                ndl[h, j+1] = b[i]
                ndl[h, j+2] = c[i]
                break
            
    for i in range(len(x)):
        
        if  ndl[i, j+1] == 0 and ndl[i, j+2] == 0:
            
            for k in range(len(a)):
        
                if  b[k] == i:
                    ndl[i, j+1] = a[k]
                    ndl[i, j+2] = c[k]
                    break
                
    for i in range(len(x)):
        
        if  ndl[i, j+1] == 0 and ndl[i, j+2] == 0:
            
            for k in range(len(a)):
        
                if  c[k] == i:
                    ndl[i, j+1] = a[k]
                    ndl[i, j+2] = b[k]
                    break

    ####################### Vertex indexes (where each vertex is) #################
                    
    v_index = np.zeros((len(a), max_nb))

    for v in range(len(x)):
        
        k = int(0)
        
        for i in range(len(a)):
            if a[i]== v or b[i]== v or c[i]== v:
                v_index[v, k] = i
                k = k + 1

    ################## Neighbor vertices ordered in clockwise or counterclockwise (it doesn't matter) ##################
              
    for h in range(len(x)):

        k = int(1)
        
        le = int(max_nb-3) #neighbor information for each vertex, neighbor data
        iteration = np.zeros(le)
        vertex = np.array(v_index[h, :le])
        
        for i in iteration:
            
            for i in vertex:
                
                if a[int(i)] == h:
                    
                    if b[int(i)] == ndl[h, k+1] and c[int(i)] != ndl[h, k]:
                        ndl[h, k+2] = c[int(i)]
                        k = k + 1
                        break
        
                    elif c[int(i)] == ndl[h, k+1] and b[int(i)] != ndl[h, k]:
                        ndl[h, k+2] = b[int(i)]
                        k = k + 1
                        break
                   
                elif b[int(i)] == h:
                    
                    if a[int(i)] == ndl[h, k+1] and c[int(i)] != ndl[h, k]:
                        ndl[h, k+2] = c[int(i)]
                        k = k + 1
                        break
                    
                    elif c[int(i)] == ndl[h, k+1] and a[int(i)] != ndl[h, k]:
                        ndl[h, k+2] = a[int(i)]
                        k = k + 1
                        break
                        
                elif c[int(i)] == h:
                    
                    if a[int(i)] == ndl[h, k+1] and b[int(i)] != ndl[h, k]:
                        ndl[h, k+2] = b[int(i)]
                        k = k + 1
                        break
                    
                    elif b[int(i)] == ndl[h, k+1] and a[int(i)] != ndl[h, k]:
                        ndl[h, k+2] = a[int(i)]
                        k = k + 1
                        break


    for i in range(len(x)):
        for j in range(3, max_nb):
            if ndl[i, j] == ndl[i, 2]:
                ndl[i, j+1:max_nb] = 0
                break
    
            
    ######################## Save to asc file #############################
    connectivity = '{h}.pial.neighbor.asc'.format(h=hemi) # first two neighbors are recurring for closing the triangle loop
    save_file = os.path.join(subjects_dir, subject, 'surf', connectivity)
    np.savetxt(save_file, ndl, fmt='%-4d', delimiter=' '' ')

    return ndl

