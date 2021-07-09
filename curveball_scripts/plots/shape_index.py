"""
- Cortical thickness distribution profiles for nine shape descriptors of shape index
for all subjects. 
- Effect sizes are calculated for each distribution combination per subject
"""

def shape_index():
    
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    import os
    import scipy.stats as stats
    
    input_txt = 'subjects_ABIDE_TD.txt'
    path = os.path.join(os.getcwd(),input_txt)
    with open(path) as f: lines = f.read().splitlines()
    
    t_cup_SI = []
    t_trough_SI = []
    t_rut_SI = []
    t_srut_SI = []
    t_saddle_SI = []
    t_sridge_SI = []
    t_ridge_SI = []
    t_dome_SI = []
    t_cap_SI = []
    
    for line in lines:
    
        hemis = ['lh','rh']
        
        for hemi in hemis:
        
            SI = '{h}.pial.SI.asc'.format(h=hemi)
            t = '{h}.thickness.asc'.format(h=hemi)
            
            subjects_name = 'subjects_ABIDE_TD'
            subjects_dir = os.path.join(os.getcwd(),subjects_name)
            subject = '{l}'.format(l=line)
            
            SI = os.path.join(subjects_dir, subject, 'surf', SI)
            t = os.path.join(subjects_dir, subject, 'surf', t)
            
            # read shape index
            with open(SI,'r') as SI_file:
                SI_lines = SI_file.readlines()
                
            SI = np.zeros(len(SI_lines))
                
            for i in range(len(SI_lines)):
                SI_data = SI_lines[i].split()
                SI[i] = SI_data[4]
                
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
                    
            for i in range(len(t)):
                if t[i] <= 0.5:
                    t[i] = 0
                    
            cup_t     = np.zeros(len(SI))
            cap_t     = np.zeros(len(SI))
            dome_t    = np.zeros(len(SI))
            trough_t = np.zeros(len(SI))
            rut_t     = np.zeros(len(SI))
            ridge_t   = np.zeros(len(SI))
            saddle_t  = np.zeros(len(SI))
            sridge_t  = np.zeros(len(SI))
            srut_t    = np.zeros(len(SI))
            
            for i in range(len(SI)):
                if SI[i] <= -0.875:
                    cup_t[i] = t[i]
                elif SI[i] > -0.875 and SI[i] <= -0.625:
                    trough_t[i] = t[i]
                elif SI[i] > -0.625 and SI[i] <= -0.375:
                    rut_t[i] = t[i]
                elif SI[i] > -0.375 and SI[i] <= -0.125:
                    srut_t[i] = t[i]
                elif SI[i] > -0.125 and SI[i] <= 0.125:
                    saddle_t[i] = t[i]
                elif SI[i] > 0.125 and SI[i] <= 0.375:
                    sridge_t[i] = t[i]
                elif SI[i] > 0.375 and SI[i] <= 0.625:
                    ridge_t[i] = t[i]
                elif SI[i] > 0.625 and SI[i] <= 0.875:
                    dome_t[i] = t[i]
                elif SI[i] >= 0.875:
                    cap_t[i] = t[i]
            
            cup_t = cup_t[cup_t != 0]
            trough_t = trough_t[trough_t != 0]
            rut_t = rut_t[rut_t != 0]
            srut_t = srut_t[srut_t != 0]
            saddle_t = saddle_t[saddle_t != 0]
            sridge_t = sridge_t[sridge_t != 0]
            ridge_t = ridge_t[ridge_t != 0]
            dome_t = dome_t[dome_t != 0]
            cap_t = cap_t[cap_t != 0]
            
            t_cup_SI = np.append(t_cup_SI, cup_t)
            t_trough_SI = np.append(t_trough_SI, trough_t)
            t_rut_SI = np.append(t_rut_SI, rut_t)
            t_srut_SI = np.append(t_srut_SI, srut_t)
            t_saddle_SI = np.append(t_saddle_SI, saddle_t)
            t_sridge_SI = np.append(t_sridge_SI, sridge_t)
            t_ridge_SI = np.append(t_ridge_SI, ridge_t)
            t_dome_SI = np.append(t_dome_SI, dome_t)
            t_cap_SI = np.append(t_cap_SI, cap_t)
        
    # Viridis Color Map
    plt.figure()
    ax = sns.kdeplot(t_cup_SI, color='#FDE725', shade=False, label='Cup',bw_adjust=5,cut=0)
    ax = sns.kdeplot(t_trough_SI, color='#B4DE2C', shade=False, label='Trough',bw_adjust=5,cut=0)
    ax = sns.kdeplot(t_rut_SI, color='#6DCD59', shade=False, label='Rut',bw_adjust=5,cut=0)
    ax = sns.kdeplot(t_srut_SI, color='#35B779', shade=False, label='Saddle_Rut',bw_adjust=5,cut=0)
    ax = sns.kdeplot(t_saddle_SI, color='#1F9E89', shade=False, label='Saddle',bw_adjust=5,cut=0)
    ax = sns.kdeplot(t_sridge_SI, color='#26828E', shade=False, label='Saddle_ridge',bw_adjust=5,cut=0)
    ax = sns.kdeplot(t_ridge_SI, color='#31688E', shade=False, label='Ridge',bw_adjust=5,cut=0)
    ax = sns.kdeplot(t_dome_SI, color='#3E4A89', shade=False, label='Dome',bw_adjust=5,cut=0)
    ax = sns.kdeplot(t_cap_SI, color='#482878', shade=False, label='Cap',bw_adjust=5,cut=0)
    ax.set(xlim=(0.5, 5))
    fname = '/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots/results_all/si_curv_all.png'
    plt.savefig(fname, dpi = 500)
        
    # Calculate Cohen's d, size of samples(n)
    n_list = {}
    
    n_list[0] = len(t_cup_SI)
    n_list[1] = len(t_trough_SI)
    n_list[2] = len(t_rut_SI)
    n_list[3] = len(t_srut_SI)
    n_list[4] = len(t_saddle_SI)
    n_list[5] = len(t_sridge_SI)
    n_list[6] = len(t_ridge_SI)
    n_list[7] = len(t_dome_SI)
    n_list[8] = len(t_cap_SI)
    
        
    # variance of the samples
    s_list = {}
    
    s_list[0] = np.var(t_cup_SI, ddof=1) 
    s_list[1] = np.var(t_trough_SI, ddof=1) 
    s_list[2] = np.var(t_rut_SI, ddof=1) 
    s_list[3] = np.var(t_srut_SI, ddof=1)
    s_list[4] = np.var(t_saddle_SI, ddof=1)
    s_list[5] = np.var(t_sridge_SI, ddof=1)
    s_list[6] = np.var(t_ridge_SI, ddof=1)
    s_list[7] = np.var(t_dome_SI, ddof=1)
    s_list[8] = np.var(t_cap_SI, ddof=1)
    
    # mean of samples
    u_list = {}
    
    u_list[0] = np.mean(t_cup_SI)
    u_list[1] = np.mean(t_trough_SI)
    u_list[2] = np.mean(t_rut_SI)
    u_list[3] = np.mean(t_srut_SI)
    u_list[4] = np.mean(t_saddle_SI)
    u_list[5] = np.mean(t_sridge_SI)
    u_list[6] = np.mean(t_ridge_SI)
    u_list[7] = np.mean(t_dome_SI)
    u_list[8] = np.mean(t_cap_SI)
        
    # calculate the pooled standard deviation
    d_all = np.zeros([9,9])
    
    for i in range(len(u_list)):
        
        for j in range(len(u_list)):
            
            sp = np.sqrt(((n_list[i] - 1) * s_list[i] + (n_list[j] - 1) * s_list[j]) / (n_list[i] + n_list[j] - 2))
        
            # calculate the effect size
            d = (u_list[j] - u_list[i]) / sp
            d_all[j,i] = d
    
    # distribution of variables
    v_list = {}
    
    v_list[0] = t_cup_SI
    v_list[1] = t_trough_SI
    v_list[2] = t_rut_SI
    v_list[3] = t_srut_SI
    v_list[4] = t_saddle_SI
    v_list[5] = t_sridge_SI
    v_list[6] = t_ridge_SI
    v_list[7] = t_dome_SI
    v_list[8] = t_cap_SI
    
    # t-test
    p_all = np.zeros([9,9])
    
    for i in range(len(v_list)):
        
        for j in range(len(v_list)):
            
            p = stats.ttest_ind(a=v_list[i], b=v_list[j], equal_var=False)
            p_val = p[1]
            p_all[j,i] = p_val
    
    # delete the cells that has p-value greater than 0.05 and effect size less than 0.02!
    # replace zeros with Nan!
    # remove upper diagonal
    
    d_all = np.tril(d_all)
    d_all[d_all == 0] = 'nan'
    
    # plot the effect size
    fig, ax = plt.subplots()
    ax = sns.heatmap(d_all, annot=True, cmap='binary', fmt=".2f", 
                annot_kws={"size":13, "family":'fantasy',"ha":'center', "weight":'book'})
    
    fname = '/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots/results_all/si_curv_effect_all.png'
    plt.savefig(fname, dpi = 500)
    
    names = [('mean_cup', 'mean_trough', 'mean_rut', 'mean_srut', 'mean_saddle', 'mean_sridge', 'mean_ridge', 'mean_dome', 'mean_cap')]
    results = [(np.mean(t_cup_SI), np.mean(t_trough_SI), np.mean(t_rut_SI), np.mean(t_saddle_SI), np.mean(t_sridge_SI), np.mean(t_ridge_SI), np.mean(t_dome_SI), np.mean(t_cap_SI))]
        
    SI_name = '/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots/results_all/si_curv_all.asc'
        
    np.savetxt(SI_name, names, fmt='%s', delimiter=' '' ') 
        
    with open(SI_name,'ab') as f:
        np.savetxt(f, results, fmt='%6.2f', delimiter=' '' ')
        
    P_name = '/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots/results_all/si_p_all.asc'
        
    np.savetxt(P_name, p_all, fmt='%6.2f', delimiter=' '' ') 
    
    return
