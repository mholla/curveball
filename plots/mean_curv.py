"""
Cortical thickness distribution profiles for positive and 
negative mean curvature with effect size for each individual

Parameters:
----------
    cortical thickness: {h}.thickness.asc for each subject
    mean curvature: {h}.pial.H.asc for each subject
    input_txt, subjects_name, output_folder: must be defined in the curveball_plots.py file
    
Returns:
-------
    Distribution profile of convex and concave points along with effect size
"""

def mean_curv(input_txt, subjects_name, output_folder):
    
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    import os
    import scipy.stats as stats
    
    path = os.path.join(os.getcwd(),input_txt)
    with open(path) as f: lines = f.read().splitlines()
    
    t_gyr_H = []
    t_sulc_H = []
    d_H =[]
    
    for line in lines:
    
        hemis = ['lh','rh']
            
        for hemi in hemis:
        
            H = '{h}.pial.H.asc'.format(h=hemi)
            t = '{h}.thickness.asc'.format(h=hemi)
            
            subjects_dir = os.path.join(os.getcwd(),subjects_name)
            subject = '{l}'.format(l=line)
            
            H = os.path.join(subjects_dir, subject, 'surf', H)
            t = os.path.join(subjects_dir, subject, 'surf', t)
            
            # read mean curvature
            with open(H,'r') as H_file:
                H_lines = H_file.readlines()
                
            H = np.zeros(len(H_lines))
                
            for i in range(len(H_lines)):
                H_data = H_lines[i].split()
                H[i] = H_data[4]
                
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
            
            H_gyr = np.zeros(len(H))
            t_gyr = np.zeros(len(t))
            H_sulc = np.zeros(len(H))
            t_sulc = np.zeros(len(t))
            
            for i in range(len(H)):
                if H[i] > 0:
                    H_sulc[i] = H[i]
                    t_sulc[i] = t[i]
                    
            for i in range(len(H)):
                if H[i] < 0:
                    H_gyr[i] = H[i]
                    t_gyr[i] = t[i]
                    
            for i in range(len(t)):
                if t_gyr[i] == 0:
                    H_gyr[i] = 0
                    
            for i in range(len(t)):
                if t_sulc[i] == 0:
                    H_sulc[i] = 0
                        
            t_gyr = t_gyr[t_gyr != 0]
            t_sulc = t_sulc[t_sulc != 0]
            
            t_gyr_H = np.append(t_gyr_H, t_gyr)
            t_sulc_H = np.append(t_sulc_H, t_sulc)
            
        # length of samples
        n1 = len(t_gyr_H)
        n2 = len(t_sulc_H)
        
        # variance of the samples
        s1 = np.var(t_gyr_H, ddof=1)
        s2 = np.var(t_sulc_H, ddof=1)
        
        # pooled standard deviation
        s = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
        
        # means of the samples
        u1 = np.mean(t_gyr_H)
        u2 = np.mean(t_sulc_H)
        
        # effect size
        d = (u1 - u2) / s
        d_H = np.append(d_H, d)
            
    plt.figure()
    ax = sns.kdeplot(t_sulc_H, color='#FDE725', shade=True, label='Positive H', bw_adjust=2, cut=0)
    bx = sns.kdeplot(t_gyr_H, color='#31688E', shade=True, label='Negative H', bw_adjust=2, cut=0)
    ax.set(xlim=(0.5, 5))
    bx.set(xlim=(0.5, 5))
    fname = os.path.join('/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots', output_folder, 'mean_curv_all.png')
    plt.savefig(fname, dpi = 500)
    
    #T-test
    p = stats.ttest_ind(a=t_sulc_H,b=t_gyr_H,equal_var=False)
    p_val = p[1]
    
    plt.figure()
    ax = sns.boxplot(data=[d_H], fliersize=0, linewidth=1, width = 0.3, boxprops={'facecolor':'None','edgecolor':'black'},
                     whiskerprops={'color':'black'},medianprops={'color':'black'},capprops={'color':'black'})
    ax = sns.stripplot(data=[d_H], color='black', size=3, alpha=0.2, zorder=0)
    ax.set(ylim=(0, 1.2))
    ax.tick_params(axis = "x", which = "both", bottom = False, top = False)
    fname = os.path.join('/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots', output_folder, 'mean_curv_effect_all.png')
    plt.savefig(fname, dpi = 500)
    
    names = [('mean_gyr', 'mean_sulc', 'std_gyr', 'std_sulc', 'p', 'mean_d')]
    results = [(np.mean(t_gyr_H), np.mean(t_sulc_H), np.std(t_gyr_H), np.std(t_sulc_H), p_val, np.mean(d_H))]
        
    H_name = os.path.join('/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots', output_folder, 'mean_curv_all.asc')
    np.savetxt(H_name, names, fmt='%s', delimiter=' '' ') 
        
    with open(H_name,'ab') as f:
        np.savetxt(f, results, fmt='%6.2f', delimiter=' '' ')
        
    return
