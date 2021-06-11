"""
Visualize the pial and alpha surface meshes for any subject using pyvista and/or open3d
"""

import numpy as np
import open3d as o3d
import os
import pyvista as pv
import scipy
import scipy.spatial
import open3d as o3d

subjects_name = 'Yale_vtk'
subjects_dir = os.path.join(os.getcwd(),subjects_name)
subject = 'Yale_0050575'

##################### obtain the point-cloud ###############################

pial_name = 'lh.pial.ply'
alpha_name = 'lh.alpha.ply'

mesh_pial = os.path.join(subjects_dir, subject, 'surf', pial_name)
mesh_alpha = os.path.join(subjects_dir, subject, 'surf', alpha_name)

mesh_alpha = pv.read(mesh_alpha)
mesh_pial = pv.read(mesh_pial)

a_bounds = mesh_alpha.bounds
p_bounds = mesh_pial.bounds

trans_ax = (abs(a_bounds[0]) + abs(a_bounds[1]))/2 + a_bounds[0]
trans_ay = (abs(a_bounds[2]) + abs(a_bounds[3]))/2 + a_bounds[2]
trans_az = (abs(a_bounds[4]) + abs(a_bounds[5]))/2 + a_bounds[4]

mesh_alpha.translate([-trans_ax, -trans_ay, -trans_az])

trans_px = (abs(p_bounds[0]) + abs(p_bounds[1]))/2 + p_bounds[0]
trans_py = (abs(p_bounds[2]) + abs(p_bounds[3]))/2 + p_bounds[2]
trans_pz = (abs(p_bounds[4]) + abs(p_bounds[5]))/2 + p_bounds[4]

mesh_pial.translate([-trans_px, -trans_py, -trans_pz])

a_center = mesh_alpha.center
p_center = mesh_pial.center

mesh_alpha.points /= 1.13 # shrink by 15%x

plotter = pv.Plotter()
# pv.set_plot_theme("document")
plotter.set_background("white")
# _ = plotter.add_mesh(mesh_pial, color='#d8dcd6', smooth_shading=True, style='surface', lighting = True, line_width = 1, opacity=1)
# _ = plotter.add_mesh(mesh_pial, show_edges=False, color=[1,1,10], line_width = .1, opacity=1, lighting = True)
_ = plotter.add_mesh(mesh_alpha, show_edges=False, lighting = True, color='lightgray', opacity=1)
cpos=[3, 0, 0]
plotter.camera_position = cpos
plotter.show()
 
#Visualize mesh with open3d
mesh_pial.compute_vertex_normals()
mesh_white.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh_pial,pcd])
o3d.visualization.draw_geometries([mesh_alpha])
o3d.visualization.draw_geometries([mesh_white])
 
