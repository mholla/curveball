"""
Cortical thickness distribution profiles for interior and exterior vertices, 
below and above the mid cortical surface with effect size per individual.
"""
def sulcal_depth():
    
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    import os
    
    input_txt = 'subjects_ABIDE_TD.txt'
    path = os.path.join(os.getcwd(),input_txt)
    with open(path) as f: lines = f.read().splitlines()
    
    t_sulc_S = []
    t_gyr_S = []
    
    d_S = []
    
    for line in lines:
        
        hemis = ['lh','rh']
        
        for hemi in hemis:
            
            S = '{h}.sulc.shrink.asc'.format(h=hemi)
            t = '{h}.thickness.asc'.format(h=hemi)
            
            subjects_name = 'subjects_ABIDE_TD'
            subjects_dir = os.path.join(os.getcwd(),subjects_name)
            subject = '{l}'.format(l=line)
            
            S = os.path.join(subjects_dir, subject, 'surf', S)
            t = os.path.join(subjects_dir, subject, 'surf', t)
            
            # read sulcal depth
            with open(S,'r') as S_file:
                S_lines = S_file.readlines()
                
            S = np.zeros(len(S_lines))
                
            for i in range(len(S_lines)):
                S_data = S_lines[i].split()
                S[i] = S_data[4]
                
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
                    
            for i in range(len(t)):
                if t[i] == 0:
                    S[i] = 0
                    
            t = t[t != 0]
            S = S[S != 0]
                    
            # Sulcal depth divided into t_sulc and t_gyral 
            S_gyr = np.zeros(len(S))
            S_sulc = np.zeros(len(S))
            
            t_gyr = np.zeros(len(t))
            t_sulc = np.zeros(len(t))
            
            for i in range(len(S)):
                if S[i] < 0:
                    S_gyr[i] = S[i]
                    t_gyr[i] = t[i]
                    
            for i in range(len(S)):
                if S[i] > 0:
                    S_sulc[i] = S[i]
                    t_sulc[i] = t[i]
                    
            t_gyr = t_gyr[t_gyr != 0]
            t_sulc = t_sulc[t_sulc != 0]
            
            S_gyr = S_gyr[S_gyr != 0]
            S_sulc = S_sulc[S_sulc != 0]
                    
            t_gyr_S = np.append(t_gyr_S, t_gyr)
            t_sulc_S = np.append(t_sulc_S, t_sulc)
    
        # sample sizes
        n1 = len(t_gyr_S)
        n2 = len(t_sulc_S)
        
        #  variance of the samples
        s1 = np.var(t_gyr_S, ddof=1)
        s2 = np.var(t_sulc_S, ddof=1)
        
        # pooled standard deviation
        s = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
        
        # means of the samples
        u1 = np.mean(t_gyr_S)
        u2 = np.mean(t_sulc_S)
        
        # effect size
        d = (u1 - u2) / s
        d_S = np.append(d_S, d)
                           
    plt.figure()
    ax = sns.kdeplot(t_gyr_S, color='#FDE725', shade=True, bw_adjust=6)
    ax = sns.kdeplot(t_sulc_S, color='#31688E', shade=True, bw_adjust= 6)
    ax.set(xlim=(0.5, 5))
    ax.set(xlim=(0.5, 5))
    fname = '/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots/results_all/sd_all.png'
    plt.savefig(fname, dpi = 500)
    
    #Box plot
    plt.figure()
    ax = sns.stripplot(data=[d_S], linewidth=0.8, color='white', edgecolor='black', size=5, alpha=0.8)
    ax = sns.boxplot(data=[d_S], fliersize=0, linewidth=1.5, width = 0.3, color='lightgrey')
    ax.set(ylim=(0, 1.2))
    fname = '/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots/results_all/sd_effect_all.png'
    plt.savefig(fname, dpi = 500)
    
    names = [('mean_gyr', 'mean_sulc', 'std_gyr', 'std_sulc')]
    results = [(np.mean(t_gyr_S), np.mean(t_sulc_S), np.std(t_gyr_S), np.std(t_sulc_S))]
        
    S_name = '/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots/results_all/sd_all.asc'
        
    np.savetxt(S_name, names, fmt='%s', delimiter=' '' ') 
        
    with open(S_name,'ab') as f:
        np.savetxt(f, results, fmt='%6.2f', delimiter=' '' ')

    return
    
    
