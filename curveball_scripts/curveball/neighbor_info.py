"""
Outputs: 
ndl: vertex neighbor information stored in a circular order (CW or CCW) at each row. 
     Column length is equal to the total number of vertices in the mesh.
     Row number is arbitrary but must be higher than the maximum number of neighbor that any vertex could have. 
     Here it is assigned as 25, which works for this particular mesh.

From here to the end of Section-2, the neighbor information for each vertex is obtained and ndl array is generated.
The purpose of this section is to store every neighbor of each vertex (in the mesh) in a circular order (clockwise or countercockwise)
in an array. First number is the vertex number and the rest are the neighbors for each row of ndl.

nb: total number of neighbors for each vertex

max_nb: Find the maximum number of neighbors that a vertex has in the mesh or set max_nb an 
arbitrarily large value (such as 25 or even 50!)
"""

def neighbor_info(a,b,c,x,y,z,subjects_dir,subject,hemi):
    
    import numpy as np
    import os
    
    # Set an arbitrarily large value for max number of neighbor that a vertex can have
    max_nb = 25

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

