#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 12:04:08 2020

@author: nagehan
"""
"""
Converting ?h.pial to stl file alters the mesh connectivity and vertex coordinates. Therefore vtk file extension will be used. 
Converting to stl file alters the connectivity (both by Freesurfer and Meshlab)
Freesurfer's ?h.pial (mesh file) is needed to be converted to ?h.pial.vtk file first, using the mris_convert Freesurfer command. (nipype is not working)
Open3D does not open vtk file. Pyvista can only open .vtk files. 
Pyvista can open .vtk files. But only mesh smoothing algorithm is Laplacian. Taubin is prefferred. 
Therefore, open the mesh file using pyvista (with the .vtk extension). Use decimation/simplification for curvature calculations.
Then save with the extension .ply. 
Open using o3d for smoothing the mesh with Laplacian and Taubin smoothing algorithms. 
Finally save the coordinates and the connectivity to a text file that is readable by Freesurfer and SurfIce.
"""

def mesh_pial_white(subjects_dir, subject, hemi):
    import open3d as o3d # used to smooth mesh
    import pyvista as pv # needed to open vtk file
    import os
    import numpy as np
    
    # Read .vtk files (changed from .asc to match ABIDE dataset)
    mesh_pial = os.path.join(subjects_dir, 'surf', '{h}.pial.vtk'.format(h=hemi))
    mesh_white = os.path.join(subjects_dir, 'surf', '{h}.white.vtk'.format(h=hemi))
    
    mesh_pial = pv.read(mesh_pial)
    mesh_white = pv.read(mesh_white)
    
    # Save as .vtk for consistency with the workflow (resave, useless if no processing occurs)
    mesh_pial.save(os.path.join(subjects_dir, 'surf', '{h}.pial.vtk'.format(h=hemi)))
    mesh_white.save(os.path.join(subjects_dir, 'surf', '{h}.white.vtk'.format(h=hemi)))
    
    # Proceed with decimation and smoothing (function used are specific to pv)
    target_reduction = 0.6 # remove 60% of original mesh
    mesh_dec_pial = mesh_pial.decimate(target_reduction)  # reduce complexity
    mesh_dec_white = mesh_white.decimate(target_reduction)
    
    mesh_smooth_pial = mesh_dec_pial.triangulate().clean().smooth(n_iter=7) # enhance quality (make polygons triangles, remove unused points, laplacian smoothing with iterations)
    mesh_smooth_white = mesh_dec_white.triangulate().clean().smooth(n_iter=7)
    
    # Save in ply format (to be opened with open3d)
    mesh_smooth_pial.save(os.path.join(subjects_dir, 'surf', '{h}.pial.ply'.format(h=hemi)))
    mesh_smooth_white.save(os.path.join(subjects_dir, 'surf', '{h}.white.ply'.format(h=hemi)))
    
    # Open .ply mesh files using open3d
    mesh_pial = os.path.join(subjects_dir, 'surf', '{h}.pial.ply'.format(h=hemi))
    mesh_white = os.path.join(subjects_dir, 'surf', '{h}.white.ply'.format(h=hemi))
    
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
    
    # Save the cleaned meshes back to .ply
    m_pial = os.path.join(subjects_dir, 'surf', '{h}.pial.ply'.format(h=hemi))
    m_white = os.path.join(subjects_dir, 'surf', '{h}.white.ply'.format(h=hemi))
    
    o3d.io.write_triangle_mesh(m_pial, mesh_pial) # saves triangle meshes to path, ?h.pial.ply
    o3d.io.write_triangle_mesh(m_white, mesh_white)
    
    # Coordinates and mesh connectivity
    v_white = np.asarray(mesh_white.vertices) # 3D coordinates of each vertices ([num of vertices, 3] array)
    tri_white = np.asarray(mesh_white.triangles) # 3D coordinates (num of vertices) of each triangle ([num of triangles, 3] array)
    
    v_pial = np.asarray(mesh_pial.vertices)
    tri_pial = np.asarray(mesh_pial.triangles)
    
    zeros = np.zeros(len(tri_pial))
    tri_p_d = np.insert(tri_pial, 3, zeros, axis=1) # add a column of zeros
    tri_p_d = tri_p_d.astype(int)
    
    zeros = np.zeros(len(tri_white))
    tri_w_d = np.insert(tri_white, 3, zeros, axis=1)
    tri_w_d = tri_w_d.astype(int)
    
    n_pial = np.array([len(v_pial), len(tri_pial)])[np.newaxis] # row vector [num vertices, num triangles]
    n_white = np.array([len(v_white), len(tri_white)])[np.newaxis]
    
    # Save connectivity and coordinates to asc file
    pial = os.path.join(subjects_dir, 'surf', '{h}.pial.asc'.format(h=hemi))
    white = os.path.join(subjects_dir, 'surf', '{h}.white.asc'.format(h=hemi))
    
    np.savetxt(pial, n_pial, fmt="%s")
    with open(pial, 'ab') as f:
        np.savetxt(f, v_pial, fmt='%10.6f', delimiter=' ')
    with open(pial, 'r') as f:
        lines = f.read().splitlines()
    with open(pial, 'w') as f:
        f.write('\n'.join([line + '  0' for line in lines]) + '\n')
    with open(pial, 'ab') as f:
        np.savetxt(f, tri_p_d, fmt='%s', delimiter=' ')
    with open(pial, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.write('#!ascii file' + '\n')
        for line in lines:
            f.write(line)
    f.close()
    
    np.savetxt(white, n_white, fmt="%s")
    with open(white, 'ab') as g:
        np.savetxt(g, v_white, fmt='%10.6f', delimiter=' ')
    with open(white, 'r') as g:
        lines = g.read().splitlines()
    with open(white, 'w') as g:
        g.write('\n'.join([line + '  0' for line in lines]) + '\n')
    with open(white, 'ab') as g:
        np.savetxt(g, tri_w_d, fmt='%s', delimiter=' ')
    with open(white, 'r+') as g:
        lines = g.readlines()
        g.seek(0)
        g.write('#!ascii file' + '\n')
        for line in lines:
            g.write(line)
    g.close()
    
    return