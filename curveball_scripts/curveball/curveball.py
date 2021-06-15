"""

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
    
    input_txt = 'subjects_yale_TD.txt'
    path = os.path.join(os.getcwd(),input_txt)
    with open(path) as f: lines = f.read().splitlines()
    
    for line in lines:
        
        subjects_name = 'Yale_vtk'
        subjects_dir = os.path.join(os.getcwd(),subjects_name)
        subject = '{l}'.format(l=line)
    
        mesh_pial_white.mesh_pial_white(subjects_dir, subject)
        
        mesh_alpha.mesh_alpha(subjects_dir, subject)
      
        x,y,z,a,b,c = coords_nodes.coords_nodes(subjects_dir,subject)
        
        neighbor_info.neighbor_info(a,b,c,x,y,z,subjects_dir,subject)
        
        Gaussian_curvature.Gaussian_curvature(x,y,z,subjects_dir,subject)
        
        mean_curvature.mean_curvature(x,y,z,subjects_dir,subject)
        
        k1_k2_SI.k1_k2_SI(x,y,z,subjects_dir,subject)
        
        cort_thick.cort_thick(subjects_dir, subject)
        
        ICI_FI_area.ICI_FI_area(subjects_dir,subject)
        
        sulcal_depth.sulcal_depth(subjects_dir, subject)
        
        region_Brodmann.region_Brodmann(a,b,c,x,y,z,subjects_dir, subject)
        
        region_Destrieux.region_Destrieux(a,b,c,x,y,z,subjects_dir, subject)
        
        smooth.smooth(subjects_dir,subject,x,y,z)
    
    return
    
curveball()









