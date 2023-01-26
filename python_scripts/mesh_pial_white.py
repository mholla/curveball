"""
Decimates and smooths the initial irregular surface mesh.

Convert ?h.pial (from Freesurfer) to vtk format using the mris_convert Freesurfer command.
Do not convert to stl format as as stl file alters the mesh connectivity and vertex coordinates.
Open3D does not open vtk file. Pyvista can only open .vtk files. But the only mesh smoothing algorithm is Laplacian. Taubin is preferred. 
Therefore, open the mesh file using pyvista (with the .vtk extension). Use decimation/simplification for curvature calculations.
Then save with the extension .ply. 
Finally save the coordinates and the connectivity to a text file that is readable by Freesurfer and SurfIce.

Parameters:
---------
    Input mesh files. If Freesurfer is used then the format is {h}.pial.vtk and {h}.white.vtk. See the instructions above. However the input mesh file
    format can also be {h}.pial.ply and {h}.white.ply
Returns:
-------
    Outputs human-readable {h}.pial.asc and {h}.white.asc text files that stores vertex coordinates and connectivity information of each mesh. 
"""

def mesh_pial_white(subjects_dir, subject, hemi):
    
    import open3d as o3d
    import pyvista as pv
    import os
    import numpy as np
        
    mesh_pial = os.path.join(subjects_dir, subject, 'surf', '{h}.pial.vtk'.format(h=hemi))
    mesh_white = os.path.join(subjects_dir, subject, 'surf', '{h}.white.vtk'.format(h=hemi))
    
    mesh_pial = pv.read(mesh_pial)
    mesh_white = pv.read(mesh_white)
    
    # Mesh decimation with pyvista
    target_reduction = 0.7 # set target reduction value (0%: no reduction, 1: 100% percent reduction)
    mesh_dec_pial = mesh_pial.decimate(target_reduction)
    mesh_dec_white = mesh_white.decimate(target_reduction)
    
    # Mesh Smoothing, cleaning, triangulation with Pyvista (Laplacian Smoothing)
    
    mesh_smooth_pial = mesh_dec_pial.triangulate().clean().smooth(n_iter=10) # set Laplacian smoothing iteration
    mesh_smooth_white = mesh_dec_white.triangulate().clean().smooth(n_iter=10) # set Laplacian smoothing iteration
    
    # Save in ply format
    mesh_smooth_pial.save(os.path.join(subjects_dir, subject, 'surf', '{h}.pial.ply'.format(h=hemi)))
    mesh_smooth_white.save(os.path.join(subjects_dir, subject, 'surf', '{h}.white.ply'.format(h=hemi)))
    
    #Open .ply mesh files using open3d
    
    mesh_pial = os.path.join(subjects_dir, subject, 'surf','{h}.pial.ply'.format(h=hemi))
    mesh_white = os.path.join(subjects_dir, subject, 'surf','{h}.white.ply'.format(h=hemi))
    
    mesh_pial = o3d.io.read_triangle_mesh(mesh_pial)
    mesh_white = o3d.io.read_triangle_mesh(mesh_white)
    
    # Clean/repair mesh
    
    mesh_pial.remove_degenerate_triangles()
    mesh_pial.remove_duplicated_triangles()
    mesh_pial.remove_duplicated_vertices()
    mesh_pial.remove_non_manifold_edges()
    mesh_pial.remove_unreferenced_vertices()
    
    mesh_white.remove_degenerate_triangles()
    mesh_white.remove_duplicated_triangles()
    mesh_white.remove_duplicated_vertices()
    mesh_white.remove_non_manifold_edges()
    mesh_white.remove_unreferenced_vertices()
    
    mesh_pial = mesh_pial.simplify_quadric_decimation(target_number_of_triangles=3200) # set target number of total triangles 
    mesh_white = mesh_white.simplify_quadric_decimation(target_number_of_triangles=3200) # set target number of total triangles
    
    mesh_pial = mesh_pial.subdivide_loop(number_of_iterations=1)
    mesh_pial = mesh_pial.subdivide_midpoint(number_of_iterations=1)
    #mesh_pial = mesh_pial.filter_smooth_laplacian(number_of_iterations=1)
    mesh_pial = mesh_pial.filter_smooth_taubin(number_of_iterations=50)
    
    mesh_white = mesh_white.subdivide_loop(number_of_iterations=1)
    mesh_white = mesh_white.subdivide_midpoint(number_of_iterations=1)
    #mesh_white = mesh_white.filter_smooth_laplacian(number_of_iterations=1)
    mesh_white = mesh_white.filter_smooth_taubin(number_of_iterations=50)
    
    mesh_pial.remove_degenerate_triangles()
    mesh_pial.remove_duplicated_triangles()
    mesh_pial.remove_duplicated_vertices()
    mesh_pial.remove_non_manifold_edges()
    mesh_pial.remove_unreferenced_vertices()
    
    mesh_white.remove_degenerate_triangles()
    mesh_white.remove_duplicated_triangles()
    mesh_white.remove_duplicated_vertices()
    mesh_white.remove_non_manifold_edges()
    mesh_white.remove_unreferenced_vertices()
    
    m_pial = os.path.join(subjects_dir, subject, 'surf','{h}.pial.smooth.ply'.format(h=hemi))
    m_white = os.path.join(subjects_dir, subject, 'surf','{h}.white.smooth.ply'.format(h=hemi))
    
    o3d.io.write_triangle_mesh(m_pial, mesh_pial)
    o3d.io.write_triangle_mesh(m_white, mesh_white)
    
    # Coordinates and mesh connectivity
                       
    v_white = np.asarray(mesh_white.vertices)
    tri_white = np.asarray(mesh_white.triangles)
    
    v_pial = np.asarray(mesh_pial.vertices)
    tri_pial = np.asarray(mesh_pial.triangles)
    
    zeros = (np.zeros(len(tri_pial)))
    tri_p_d = np.insert(tri_pial, 3, zeros, axis=1)
    tri_p_d = tri_p_d.astype(int)
    
    zeros = (np.zeros(len(tri_white)))
    tri_w_d = np.insert(tri_white, 3, zeros, axis=1)
    tri_w_d = tri_w_d.astype(int)
    
    n_pial = np.array([len(v_pial),len(tri_pial)])[np.newaxis] # takes the transpose of 1D array
    n_white = np.array([len(v_white),len(tri_white)])[np.newaxis]
    
    # Save connectivity and coordinates to asc file (Surfice - Freesurfer readable)
    
    pial = os.path.join(subjects_dir, subject, 'surf','{h}.pial.asc'.format(h=hemi))
    white = os.path.join(subjects_dir, subject, 'surf','{h}.white.asc'.format(h=hemi))
    
    # Write pial mesh to txt file
    
    np.savetxt(pial, n_pial, fmt="%s") 
    with open(pial,'ab') as f:
        np.savetxt(f, v_pial, fmt='%10.6f', delimiter=' '' ')
    with open(pial, 'r') as f:
        lines = f.read().splitlines()
    with open(pial, 'w') as f: 
        f.write('\n'.join([line + '  0' for line in lines])+ '\n')  
    with open(pial,'ab') as f:
        np.savetxt(f, tri_p_d, fmt='%s', delimiter=' '' ')
    f = open(pial,'r+')
    lines = f.readlines() # read old content
    f.seek(0) # go back to the beginning of the file
    f.write('#!ascii file' + '\n') # write new content at the beginning
    for line in lines: # write old content after new
        f.write(line)
    f.close()
    
    # Write white mesh to txt file
    
    np.savetxt(white, n_white, fmt="%s")
    with open(white,'ab') as g:
        np.savetxt(g, v_white, fmt='%10.6f', delimiter=' '' ')
    with open(white, 'r') as g:
        lines = g.read().splitlines()
    with open(white, 'w') as g: 
        g.write('\n'.join([line + '  0' for line in lines])+ '\n')  
    with open(white,'ab') as g:
        np.savetxt(g, tri_w_d, fmt='%s', delimiter=' '' ')
    g = open(white,'r+')
    lines = g.readlines() # read old content
    g.seek(0) # go back to the beginning of the file
    g.write('#!ascii file' + '\n') # write new content at the beginning
    for line in lines: # write old content after new
        g.write(line)
    g.close()
    
    return 
  

