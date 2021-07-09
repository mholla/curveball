"""
Main script of the pipeline. Run this only. Brief instructions are as follows:
    
mesh_pial_white: decimates and smoothens the pial and white triangular surface meshes
mesh_alpha: alpha surface is generated and saved as .ply from the pial surface
cort_thick: calculates the cortical thickness from smooth white and pial surface meshes, average thickness is taken.
sulcal_depth: sulcal depth is calculated using the alpha surface
coords_nodes: vertex coordinates (x,y,z) and triangle connectivity (a,b,c) of each mesh for each hemisphere
neighbor_info: neighbors of each vertex
Gaussian_curvature: calculates the Gaussian curvature surface area for each vertex
mean_curvature: calculates the mean curvature for each vertex
k1_k2_SI: calculates the principal curvatures (K1 and k2) and shape index (SI) for each vertex
ICI_FI_area: calculates the total normalized intrinsic curvature index, total folding index, and surface area for all convex, concave, and saddle shaped points
region_Brodmann: surface data are labelled and extracted for each region of the Brodmann atlas
region_Destrieux: surface data are labelled and extracted for each region of the Destrieux atlas
smooth: surface data are smoothed with two iterations
t_ratio: calculates cortical thickness ratio (tg/ts) for different coverage ratio
"""

def curveball():
    
    import os
    import coords_nodes
    import neighbor_info
    import mesh_pial_white
    import mesh_alpha
    import Gaussian_curvature
    import mean_curvature
    import k1_k2_SI
    import ICI_FI_area
    import cort_thick
    import sulcal_depth
    import smooth
    import region_Destrieux
    import region_Brodmann
    import t_ratio
    
    input_txt = 'subjects_ABIDE_TD.txt'
    path = os.path.join(os.getcwd(),input_txt)
    with open(path) as f: lines = f.read().splitlines()
    
    for line in lines:
        
        subjects_name = 'subjects_ABIDE_TD'
        subjects_dir = os.path.join(os.getcwd(),subjects_name)
        subject = '{l}'.format(l=line)
        
        hemis = ['lh','rh']
        
        for hemi in hemis:
            
            mesh_pial_white.mesh_pial_white(subjects_dir, subject, hemi)
        
            mesh_alpha.mesh_alpha(subjects_dir, subject, hemi)
        
            cort_thick.cort_thick(subjects_dir, subject, hemi)
        
            sulcal_depth.sulcal_depth(subjects_dir, subject, hemi)
      
            x,y,z,a,b,c = coords_nodes.coords_nodes(subjects_dir,subject, hemi)
            
            neighbor_info.neighbor_info(a,b,c,x,y,z,subjects_dir,subject,hemi)
            
            Gaussian_curvature.Gaussian_curvature(x,y,z,subjects_dir,subject,hemi)
            
            mean_curvature.mean_curvature(x,y,z,subjects_dir,subject,hemi)
            
            k1_k2_SI.k1_k2_SI(x,y,z,subjects_dir,subject,hemi)
            
            ICI_FI_area.ICI_FI_area(subjects_dir,subject,hemi)
            
            smooth.smooth(subjects_dir,subject,x,y,z,hemi)
            
            region_Brodmann.region_Brodmann(a,b,c,x,y,z,subjects_dir, subject,hemi)
            
            region_Destrieux.region_Destrieux(a,b,c,x,y,z,subjects_dir, subject,hemi)
            
            t_ratio.t_ratio(subjects_dir,subject,hemi)
    
    return
    
curveball()









