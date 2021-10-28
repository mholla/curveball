"""
Main plotting script of the pipeline. Plots curvature and thickness distributions.
    
"""

def curveball_plots():
    
    import os
    import g_curv
    import mean_curv
    import shape_index
    import sulcal_depth
    import CT
    import H
    import K
    import SI
    import H_S
    import K_S
    import SI_S
    import ICI_FI_area

    input_txt = 'subjects_ABIDE_TD_quality.txt'
    subjects_name = 'subjects_ABIDE_TD'
    output_folder = 'results_ABIDE_TD'
        
    mean_curv.mean_curv(input_txt, subjects_name, output_folder)
    g_curv.g_curv(input_txt, subjects_name, output_folder)
    shape_index.shape_index(input_txt, subjects_name, output_folder)
    sulcal_depth.sulcal_depth()
    H_S.H_S(input_txt, subjects_name, output_folder)
    K_S.K_S(input_txt, subjects_name, output_folder)
    SI_S.SI_S(input_txt, subjects_name, output_folder)
    CT.CT(input_txt, subjects_name, output_folder)
    H.H(input_txt, subjects_name, output_folder)
    SI.SI(input_txt, subjects_name, output_folder)
    K.K(input_txt, subjects_name, output_folder)
    ICI_FI_area(input_txt, subjects_name, output_folder)
        
    return
    
curveball_plots()









