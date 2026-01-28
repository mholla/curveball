"""
Parameters:
---------
   pial surface mesh: {h}.pial.ply
   alpha surface mesh: {h}.alpha.ply
   
Returns:
-------
   major sulcal depth: {h}.sulc.asc
   shrunken sulcal depth: {h}.sulc.shrink.asc
"""

def sulcal_depth(subjects_dir, subject, hemi):
    import numpy as np
    import scipy
    import scipy.spatial
    import pyvista as pv
    import os
    
    mesh_pial = '{h}.pial.ply'.format(h=hemi)
    mesh_alpha = '{h}.alpha.ply'.format(h=hemi)
    
    # Fixed path
    mesh_pial = os.path.join(subjects_dir, 'surf', mesh_pial)
    mesh_alpha = os.path.join(subjects_dir, 'surf', mesh_alpha)
    
    mesh_pial = pv.read(mesh_pial)
    mesh_alpha = pv.read(mesh_alpha)
    
    s = np.zeros(len(mesh_pial.points)) # array the length of the number of vertices
    
    # why not use the KDTree again? (from what i see this is slower)
    for i in range(len(mesh_pial.points)):
        dist = scipy.spatial.distance.cdist(mesh_alpha.points, mesh_pial.points[[i]], metric='euclidean') # computes euclidean distance from a pial point to all points on alpha mesh
        index = np.where(dist == dist.min()) # finds index where the euclidean distance is at a minimum (index of closest alpha mesh index)
        s[i] = dist[index[0][0]] # save minimum distance to array
    
    # Fixed path
    sulc = os.path.join(subjects_dir, 'surf', '{h}.sulc.asc'.format(h=hemi))
    
    indices = np.array(range(len(s)))
    columns = np.column_stack([mesh_pial.points, s])
    
    np.savetxt(sulc, indices, fmt='%03d', delimiter=' ') 
    
    with open(sulc, 'r') as f:
        lines = f.read().splitlines()
    with open(sulc, 'w') as f: 
        for i in range(len(columns)):
            f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i, 0]) + ' ' + '%10.6f' % (columns[i, 1])
                             + ' ' + '%10.6f' % (columns[i, 2]) + ' ' + '%10.6f' % (columns[i, 3])]) + '\n')    
    
    """ Calculate sulcal depth for isometrically (15%) shrunken alpha surface mesh
    First, center each mesh to the origin point (0,0,0)"""
    a_center = mesh_alpha.center # find the coordinates for the center of the mesh
    p_center = mesh_pial.center

    mesh_alpha.translate([-a_center[0], -a_center[1], -a_center[2]]) # shift the mesh so that the center coordinate becomes (0,0,0)
    mesh_pial.translate([-p_center[0], -p_center[1], -p_center[2]])
    
    magnitude = np.zeros(len(mesh_alpha.points))
    offset = np.zeros(len(mesh_alpha.points))
    
    for i in range(len(mesh_alpha.points)):
        magnitude[i] = np.linalg.norm(mesh_alpha.points[i]) # sqrt(x^2+y^2+z^2), how far vertex is from center
        # uses 7mm so that roughly half of the vertices are outside the midcortical surface and half are inside
        offset[i] = (magnitude[i] - 7)/magnitude[i] # relative offsetfrom 7mm sphere, positive if outside sphere
    
    for i in range(len(mesh_alpha.points)): # shrink alpha mesh (still don't really understand how and why this is 15%)
        mesh_alpha.points[i] *= offset[i] # multiplies offset by points and replaces value in mesh_alpha
    
    s_shrink = np.zeros(len(mesh_pial.points))
    
    for i in range(len(mesh_pial.points)):
        dist = scipy.spatial.distance.cdist(mesh_alpha.points, mesh_pial.points[[i]], metric='euclidean')
        index = np.where(dist == dist.min())
        s_shrink[i] = dist[index[0][0]]
        
        # pial layer vertex values
        p_x = mesh_pial.points[i, 0]
        p_y = mesh_pial.points[i, 1]
        p_z = mesh_pial.points[i, 2]
        
        # nearest shrunken alpha layer vertex values
        a_sx = mesh_alpha.points[index[0][0], 0]
        a_sy = mesh_alpha.points[index[0][0], 1]
        a_sz = mesh_alpha.points[index[0][0], 2]
        
        # checks if shrunken alpha layer is further from origin than pial layer
        if np.sqrt(p_x*p_x + p_y*p_y + p_z*p_z) < np.sqrt(a_sx*a_sx + a_sy*a_sy + a_sz*a_sz):
            s_shrink[i] = -s_shrink[i] # flips sign on distance (indicates pial point is inside alpha surface)
    
    # Fixed path
    sulc = os.path.join(subjects_dir, 'surf', '{h}.sulc.shrink.asc'.format(h=hemi))
    
    indices = np.array(range(len(s_shrink)))
    columns = np.column_stack([mesh_pial.points, -s_shrink])
    
    np.savetxt(sulc, indices, fmt='%03d', delimiter=' ') 
    
    with open(sulc, 'r') as f:
        lines = f.read().splitlines()
    with open(sulc, 'w') as f: 
        for i in range(len(columns)):
            f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i, 0]) + ' ' + '%10.6f' % (columns[i, 1])
                             + ' ' + '%10.6f' % (columns[i, 2]) + ' ' + '%10.6f' % (columns[i, 3])]) + '\n')    
        
    return