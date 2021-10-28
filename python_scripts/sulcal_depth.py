"""
Parameters:
---------
   pial surface mesh: {h}.pial.ply
   alpha surface mesh: {h}.pial.ply
   
Returns:
-------
   major sulcal depth: {h}.sulc.asc
   shrunken sulcal depth: {h}.sulc.shrink.asc'
"""

def sulcal_depth(subjects_dir, subject, hemi):
    
    import numpy as np
    import scipy
    import scipy.spatial
    import pyvista as pv
    import os
    
    mesh_pial = '{h}.pial.ply'.format(h=hemi)
    mesh_alpha = '{h}.alpha.ply'.format(h=hemi)
    
    mesh_pial = os.path.join(subjects_dir, subject, 'surf', mesh_pial)
    mesh_alpha = os.path.join(subjects_dir, subject, 'surf', mesh_alpha)
    
    mesh_pial = pv.read(mesh_pial)
    mesh_alpha = pv.read(mesh_alpha)
    
    s = np.zeros(len(mesh_pial.points))
    
    for i in range(len(mesh_pial.points)):
        
        dist = scipy.spatial.distance.cdist(mesh_alpha.points, mesh_pial.points[[i]], metric='euclidean')
        
        index = np.where(dist == dist.min())
        s[i] = dist[index[0][0]]
    
    sulc = os.path.join(subjects_dir, subject, 'surf', '{h}.sulc.asc'.format(h=hemi))
    
    indices = np.array(range(len(s)))
    columns = np.column_stack([mesh_pial.points, s])
    
    np.savetxt(sulc, indices, fmt='%03d', delimiter=' '' ') 
    
    with open(sulc,'r') as f:
        lines = f.read().splitlines()
    with open(sulc, 'w') as f: 
        for i in range(len(columns)):
            f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i,0])  + ' ' + '%10.6f' % (columns[i,1])
            + ' ' + '%10.6f' % (columns[i,2]) + ' ' + '%10.6f' % (columns[i,3])])+ '\n')    
    
    """ Calculate sulcal depth for isometrically (15%) shrunken alpha surface mesh
    First, center each mesh to the origin point (0,0,0)"""
    
    a_center = mesh_alpha.center
    p_center = mesh_pial.

    mesh_alpha.translate([-a_center[0], -a_center[1], -a_center[2]])
    mesh_pial.translate([-p_center[0], -p_center[1], -p_center[2]])
    
    magnitude = np.zeros(len(mesh_alpha.points))
    offset = np.zeros(len(mesh_alpha.points))
    
    for i in range(len(mesh_alpha.points)):
        
        magnitude[i] = np.linalg.norm(mesh_alpha.points[i])
        offset[i] = (magnitude[i] - 7)/magnitude[i]
    
    for i in range(len(mesh_alpha.points)):
        mesh_alpha.points[i] *= offset[i]
    
    s_shrink = np.zeros(len(mesh_pial.points))
    
    for i in range(len(mesh_pial.points)):
        
        dist = scipy.spatial.distance.cdist(mesh_alpha.points, mesh_pial.points[[i]], metric='euclidean')
        
        index = np.where(dist == dist.min())
        s_shrink[i] = dist[index[0][0]]
        
        p_x = mesh_pial.points[i,0]
        p_y = mesh_pial.points[i,1]
        p_z = mesh_pial.points[i,2]
        
        a_sx = mesh_alpha.points[index[0][0],0]
        a_sy = mesh_alpha.points[index[0][0],1]
        a_sz = mesh_alpha.points[index[0][0],2]
        
        if np.sqrt(p_x*p_x + p_y*p_y + p_z*p_z) < np.sqrt(a_sx*a_sx + a_sy*a_sy + a_sz*a_sz):
            
            s_shrink[i] = -s_shrink[i]
    
    sulc = os.path.join(subjects_dir, subject, 'surf', '{h}.sulc.shrink.asc'.format(h=hemi))
    
    indices = np.array(range(len(s_shrink)))
    columns = np.column_stack([mesh_pial.points, -s_shrink])
    
    np.savetxt(sulc, indices, fmt='%03d', delimiter=' '' ') 
    
    with open(sulc,'r') as f:
        lines = f.read().splitlines()
    with open(sulc, 'w') as f: 
        for i in range(len(columns)):
            f.write('\n'.join([lines[i] + ' ' + '%10.6f' % (columns[i,0])  + ' ' + '%10.6f' % (columns[i,1])
            + ' ' + '%10.6f' % (columns[i,2]) + ' ' + '%10.6f' % (columns[i,3])])+ '\n')    
        
    return 



