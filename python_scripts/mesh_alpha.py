"""
Alpha mesh generation from pial surface mesh point cloud. Alpha surface tight wraps the pial surface.

Parameters:
---------
    Reads {h}.pial.ply mesh file

Returns:
-------
    Outputs {h}.alpha.ply and {h}.alpha.vtk alpha-mesh files. The output file format can be changed accordingly.
"""

def mesh_alpha(subjects_dir, subject, hemi):
    import open3d as o3d
    import os
    import pyvista as pv
        
    # Get the point-cloud
    pial_name = '{h}.pial.ply'.format(h=hemi)
    alpha_name = '{h}.alpha.ply'.format(h=hemi)
    
    # Fixed path: Remove 'subject' since subjects_dir is the full path
    mesh_pial = os.path.join(subjects_dir, 'surf', pial_name)
    mesh_pial = o3d.io.read_triangle_mesh(mesh_pial)
    pial_points = mesh_pial.vertices 
    
    pcd = o3d.geometry.PointCloud() # creates pointcloud (what is that?)
    pcd.points = o3d.utility.Vector3dVector(pial_points) # assigns mesh vertices to pointcloud
    
    alpha = 20 # defines complexity
    mesh_alpha = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha) # create triangle mesh
    mesh_alpha.compute_vertex_normals() # normalized vertices
    
    mesh_alpha = mesh_alpha.subdivide_loop(number_of_iterations=1) # smooths by adding more triangles
    mesh_alpha = mesh_alpha.subdivide_midpoint(number_of_iterations=1)
    mesh_alpha = mesh_alpha.filter_smooth_laplacian(number_of_iterations=5)
    mesh_alpha = mesh_alpha.filter_smooth_taubin(number_of_iterations=50)
    
    # clean/repair
    mesh_alpha.remove_degenerate_triangles()
    mesh_alpha.remove_duplicated_triangles()
    mesh_alpha.remove_duplicated_vertices()
    mesh_alpha.remove_non_manifold_edges()
    
    # Fixed path for saving
    alpha = os.path.join(subjects_dir, 'surf', alpha_name)
    o3d.io.write_triangle_mesh(alpha, mesh_alpha)
    
    mesh_alpha = pv.read(alpha)
    # Save in vtk format
    mesh_alpha.save(os.path.join(subjects_dir, 'surf', '{h}.alpha.vtk'.format(h=hemi)))
    # Save in ply format
    mesh_alpha.save(os.path.join(subjects_dir, 'surf', '{h}.alpha.ply'.format(h=hemi)))
    
    return