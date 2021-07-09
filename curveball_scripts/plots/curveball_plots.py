"""
Main plotting script of the pipeline. Plots curvature and thickness distributions of each subset of the ABIDE dataset.
    
"""

def curveball_plots():
    
    import g_curv
    import mean_curv
    import shape_index
    import sulcal_depth
    import CT
    import H
    import K
    import SI
        
    mean_curv.mean_curv()
    g_curv.g_curv()
    shape_index.shape_index()
    sulcal_depth.sulcal_depth()
    CT.CT()
    H.H()
    SI.SI()
    K.K()
        
    return
    
curveball_plots()









