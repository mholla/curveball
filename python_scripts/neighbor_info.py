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

def neighbor_info(a, b, c, x, y, z, subjects_dir, subject, hemi):
    import numpy as np
    import os
    
    # Set an arbitrarily large value for max number of neighbor that a vertex can have
    max_nb = 35

    # Build a vertex-to-triangle mapping for faster lookup
    num_vertices = len(x)
    num_triangles = len(a)
    vertex_to_triangles = [[] for _ in range(num_vertices)] # initializes an empty list for each vertex
    
    for i in range(num_triangles):
        v1, v2, v3 = int(a[i]), int(b[i]), int(c[i]) # extracts each vertex index for a triangle
        # appends triangle index (column wise) to vertex index row 
        vertex_to_triangles[v1].append(i)
        vertex_to_triangles[v2].append(i)
        vertex_to_triangles[v3].append(i)

    # Initialize neighbor array
    ndl = np.zeros((num_vertices, max_nb)) 
    for i in range(num_vertices):
        ndl[i, 0] = i # set first column to be 0 to num vertices - 1

    # Find the first two neighbors for each vertex (assigns to second and third column for that vertex)
    for h in range(num_vertices):
        found = False
        for tri_idx in vertex_to_triangles[h]: # searches through triangles associated with h vertex
            if a[tri_idx] == h:
                ndl[h, 1] = b[tri_idx]
                ndl[h, 2] = c[tri_idx]
                found = True
                break
            elif b[tri_idx] == h:
                ndl[h, 1] = a[tri_idx]
                ndl[h, 2] = c[tri_idx]
                found = True
                break
            elif c[tri_idx] == h:
                ndl[h, 1] = a[tri_idx]
                ndl[h, 2] = b[tri_idx]
                found = True
                break
        if not found:
            # If no triangle contains this vertex, set neighbors to 0
            ndl[h, 1] = 0
            ndl[h, 2] = 0

    # Find remaining neighbors in a circular order
    for h in range(num_vertices):
        if ndl[h, 1] == 0 and ndl[h, 2] == 0:
            continue  # Skip vertices with no neighbors
        k = 1
        le = max_nb - 3
        while k < le:
            found_next = False
            for tri_idx in vertex_to_triangles[h]:
                v1, v2, v3 = a[tri_idx], b[tri_idx], c[tri_idx]
                if v1 == h:
                    if v2 == ndl[h, k+1] and v3 != ndl[h, k]:
                        ndl[h, k+2] = v3
                        k += 1
                        found_next = True
                        break
                    elif v3 == ndl[h, k+1] and v2 != ndl[h, k]:
                        ndl[h, k+2] = v2
                        k += 1
                        found_next = True
                        break
                elif v2 == h:
                    if v1 == ndl[h, k+1] and v3 != ndl[h, k]:
                        ndl[h, k+2] = v3
                        k += 1
                        found_next = True
                        break
                    elif v3 == ndl[h, k+1] and v1 != ndl[h, k]:
                        ndl[h, k+2] = v1
                        k += 1
                        found_next = True
                        break
                elif v3 == h:
                    if v1 == ndl[h, k+1] and v2 != ndl[h, k]:
                        ndl[h, k+2] = v2
                        k += 1
                        found_next = True
                        break
                    elif v2 == ndl[h, k+1] and v1 != ndl[h, k]:
                        ndl[h, k+2] = v1
                        k += 1
                        found_next = True
                        break
            if not found_next or ndl[h, k+2] == ndl[h, 2]:
                break

    # Clean up: Set remaining entries to 0 after finding the cycle
    for i in range(num_vertices):
        for j in range(3, max_nb):
            if ndl[i, j] == ndl[i, 2]:
                ndl[i, j+1:max_nb] = 0
                break
    
    # Save to asc.ConcurrentModificationException file
    connectivity = '{h}.pial.neighbor.asc'.format(h=hemi)
    save_file = os.path.join(subjects_dir, 'surf', connectivity)
    np.savetxt(save_file, ndl, fmt='%-4d', delimiter=' ')

    return ndl