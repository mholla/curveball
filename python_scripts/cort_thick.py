"""
Parameters:
---------
subjects directory, subject name, hemi (should be defined in the main script curveball.py)

reads {h}.pial.ply and {h}.white.ply (outputs from mesh_pial_white.py scrips) files to
calculate the cortical thickness for each hemisphere. 

Returns: 
--------
{h}.thickness.asc for each hemisphere
"""

def cort_thick(subjects_dir, subject, hemi):
    import numpy as np
    from scipy.spatial import KDTree
    import pyvista as pv
    import os
        
    mesh_pial = '{h}.pial.ply'.format(h=hemi)
    mesh_white = '{h}.white.ply'.format(h=hemi)
    
    # Fixed path
    mesh_pial = os.path.join(subjects_dir, 'surf', mesh_pial)
    mesh_white = os.path.join(subjects_dir, 'surf', mesh_white)
    
    mesh_pial = pv.read(mesh_pial)
    mesh_white = pv.read(mesh_white)
    
    pial_points = mesh_pial.points # array of the 3D vertex coordinates      
    white_points = mesh_white.points  
    
    # pial
    tree = KDTree(white_points) # creates data structure for nearest-neighbor queries
    t1, idx1 = tree.query(pial_points) # array of euclidean distances from each pial point to nearest white point, index of each white point
    
    # white
    tree2 = KDTree(pial_points)
    t2, idx2 = tree2.query(white_points)
    
    # Cortical thickness for pial surface, for white surface calculations use the formula below!
    t_ave = np.zeros(len(t1))
    for i in range(len(t1)):
        # average distance between nearest pial and white point for each white point index
        t_ave[i] = (t1[i] + t2[idx1[i]])/2
    
    # # Cortical thickness for white surface
    # t_ave = np.zeros(len(t2))
    # for i in range(len(t2)):
    #     t_ave[i] = (t2[i] + t1[idx2[i]])/2
    
    # Fixed path
    thick = os.path.join(subjects_dir, 'surf', '{h}.thickness.asc'.format(h=hemi))
    
    indices = np.array(range(len(t_ave)))
    columns = np.column_stack([mesh_pial.points, t_ave])
    
    np.savetxt(thick, indices, fmt='%03d', delimiter=' ') 
    
    with open(thick, 'r') as f:
        lines = f.read().splitlines()
    with open(thick, 'w') as f: 
        for i in range(len(columns)):
            f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i, 0]) + ' ' + '%10.6f' % (columns[i, 1])
                             + ' ' + '%10.6f' % (columns[i, 2]) + ' ' + '%10.6f' % (columns[i, 3])]) + '\n') 

    return