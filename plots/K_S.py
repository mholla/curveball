"""
Variation of average cortical thickness with respect to Gaussian curvature and sulcal depth 
for each subject. Gaussian curvature and sulcal depth is divided into 20 linearly spaced intervals


Parameters:
---------
    sulcal depth: {h}.sulc.shrink.asc file for each subject
    cortical thickness: {h}.thickness.asc file for each subject
    mean curvature: {h}.pial.H.asc file for each subject

Returns:
-------
    t_map: average cortical thickness map for each subject bounded by Gaussian curvature and sulcal depth
    t_map_list: average cortical thickness map of each subject saved in a list
    t_ave_map: average cortical thickness map averaged over all subjects
    
    ind_map: average of total number of vertices map for each bounded region (for each subject)
    ind_map_list: average vertices map of each subject saved in a list
    ind_ave_map: average vertices map averaged over all subjects
"""

def K_S(input_txt, subjects_name, output_folder):
    
    import numpy as np
    import os
    import heatmap_circle

    path = os.path.join(os.getcwd(),input_txt)
    with open(path) as f: lines = f.read().splitlines()
    
    t_map_list = {}
    ind_map_list = {}
    vertices = {}
    
    for line in lines:
        
        K_all = []
        t_all = []
        S_all = []
        
        hemis = ['lh','rh']
            
        for hemi in hemis:
        
            subjects_dir = os.path.join(os.getcwd(),subjects_name)
            subject = '{l}'.format(l=line)
        
            S = '{h}.sulc.shrink.asc'.format(h=hemi)
            t = '{h}.thickness.asc'.format(h=hemi)
            K = '{h}.pial.K.asc'.format(h=hemi)
        
            S = os.path.join(subjects_dir, subject, 'surf', S)
            t = os.path.join(subjects_dir, subject, 'surf', t)
            K = os.path.join(subjects_dir, subject, 'surf', K)
        
            # read sulcal depth
            with open(S,'r') as S_file:
                S_lines = S_file.readlines()
                
            S = np.zeros(len(S_lines))
                
            for i in range(len(S_lines)):
                S_data = S_lines[i].split()
                S[i] = S_data[4]
                
            # read mean curvature
            with open(K,'r') as K_file:
                K_lines = K_file.readlines()
                
            K = np.zeros(len(K_lines))
                
            for i in range(len(K_lines)):
                K_data = K_lines[i].split()
                K[i] = K_data[4]
                
            # read cortical thickness
            with open(t,'r') as t_file:
                t_lines = t_file.readlines()
                
            t = np.zeros(len(t_lines))
                
            for i in range(len(t_lines)):
                t_data = t_lines[i].split()
                t[i] = t_data[4]
                
            for i in range(len(t)):
                if t[i] >= 5:
                    t[i] = 0
                    S[i] = 0
                    K[i] = 0
                    
            for i in range(len(t)):
                if t[i] <= 0.5:
                    t[i] = 0
                    S[i] = 0
                    K[i] = 0
                           
            for i in range(len(S)):
                if S[i] == 0:
                    t[i] = 0
                    K[i] = 0
                    
            for i in range(len(K)):
                if K[i] == 0:
                    t[i] = 0
                    S[i] = 0
                    
            K = K[K != 0]
            t = t[t != 0]   
            S = S[S != 0]
            
            K_all = np.append(K_all, K)
            t_all = np.append(t_all, t)
            S_all = np.append(S_all, S)
            # end of reading data
            
        # range of sulcal depth    
        div = 20
        s = np.around(np.linspace(min(S_all), max(S_all), div), decimals=1)
        
        k_s = np.zeros((len(s)-1, len(K_all)))
        t_s = np.zeros((len(s)-1, len(t_all)))
        
        for j in range(len(s) - 1):
            
            for i in range(len(S_all)):
                
                if S_all[i] >= s[j] and S_all[i] < s[j + 1]:
                    k_s[j, i] = K_all[i]
                    t_s[j, i] = t_all[i]
        
        # range of Gaussian curvature
        l = np.around(np.linspace(-0.05, 0.05, div), decimals=3) 
        
        t_map= np.zeros((len(s)-1, len(l)-1))
        ind_map = np.zeros((len(s)-1, len(l)-1))
        
        for k in range(len(s)-1):
            
            t_n = np.zeros((len(l)-1, len(t_all)))
        
            for j in range(len(l)-1):
        
                for i in range(len(K_all)):
                
                    if k_s[k,i] >= l[j] and k_s[k,i] < l[j + 1]:
                        t_n[j, i] = t_s[k,i]
                    
                d = t_n[j][t_n[j] != 0]        
                t_map[k,j] = np.mean(d)
                ind_map[k,j] = len(d)
        
        t_map = np.transpose(t_map)
        ind_map = np.transpose(ind_map)
        
        NaNs = np.isnan(t_map) # Replace nans with zeros in the t_map array
        t_map[NaNs] = 0
        
        t_map_list['t_map_{l}'.format(l=line)] = t_map
        ind_map_list['ind_map_{l}'.format(l=line)] = ind_map
        vertices['{l}'.format(l=line)] = len(K_all)
        
    # reduce the subjects that has zero thickness mean before averaging over all subjects
    subj_map = np.zeros([len(t_map),len(t_map)])
    
    for i in range(len(subj_map)):
        subj_map[i] = len(lines)
    
        
    for i in range(len(s)-1):
        
        for j in range(len(s)-1):
            
            for line in lines:
    
                subjects_dir = os.path.join(os.getcwd(),subjects_name)
                subject = '{l}'.format(l=line)
                
                if t_map_list['t_map_{l}'.format(l=line)][i][j] == 0 or ind_map_list['ind_map_{l}'.format(l=line)][i][j] == 0:
                    
                    subj_map[i][j] = subj_map[i][j]-1
    
    t_ave_map = np.zeros([len(t_map),len(t_map)])
    ind_ave_map = np.zeros([len(t_map),len(t_map)])
                    
    for line in lines:
        
        subjects_name = 'subjects_ABIDE_TD'
        subjects_dir = os.path.join(os.getcwd(),subjects_name,subjects_name)
        subject = '{l}'.format(l=line)
        
        t_ave_map = t_ave_map + t_map_list['t_map_{l}'.format(l=line)]
        ind_ave_map = ind_ave_map + ind_map_list['ind_map_{l}'.format(l=line)]
        
    t_ave_map = t_ave_map / subj_map
    ind_ave_map = ind_ave_map / subj_map
    
    file = os.path.join('/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots', output_folder, 'k_s_t.npy')
    np.save(file, t_ave_map)
    
    file = os.path.join('/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots', output_folder, 'k_s_ind.npy')
    np.save(file, ind_ave_map)
    
    """
    Call heatmap_circle.py script to plot the heatmap
    Cortical thickness map with size of circles indicating total number of vertices
    """
    
    heatmap_circle.heatmap_circle(t_ave_map, ind_ave_map, s, l)
    
    return
