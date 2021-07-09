"""
Cortical thickness distribution profile for all subjects
"""
def CT():
    
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    import os
    from scipy.stats import skew
    
    input_txt = 'subjects_ABIDE_TD.txt'
    path = os.path.join(os.getcwd(),input_txt)
    with open(path) as f: lines = f.read().splitlines()
    
    t_all = []
    
    for line in lines:
        
        hemis = ['lh','rh']
        
        for hemi in hemis:
        
            t = '{h}.thickness.asc'.format(h=hemi)
            
            subjects_name = 'subjects_ABIDE_TD'
            subjects_dir = os.path.join(os.getcwd(),subjects_name)
            subject = '{l}'.format(l=line)
            
            t = os.path.join(subjects_dir, subject, 'surf', t)
                
            # reading cortical thickness   
            with open(t,'r') as t_file:
                t_lines = t_file.readlines()    
            
            t = np.zeros(len(t_lines))
            
            for i in range(len(t_lines)):
                t_data = t_lines[i].split()
                t[i] = t_data[4]
                
            t[t <= 0.5] = 0
            t[t >= 5] = 0
            t = t[t != 0]
        
            t_all = np.append(t_all, t)
    
    plt.figure()
    sns.kdeplot(t_all, color='#3E4A89', shade=True, bw_adjust=6, label='Cortical thickness')
    plt.legend(loc='best', prop={'size': 12})
    fname = '/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots/results_age/ct_all.png'
    plt.savefig(fname, dpi = 500)
    
    #Statistic
    var = np.var(t_all)
    mean = np.mean(t_all)
    skew = skew(t_all)
    std = np.std(t_all)
    
    names = [('CT_mean', 'CT_std', 'CT_var', 'CT_skew')]
    results = [(mean, std, var, skew)]
        
    CT_name = '/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots/results_age/ct_all.asc'
        
    np.savetxt(CT_name, names, fmt='%s', delimiter=' '' ') 
        
    with open(CT_name,'ab') as f:
        np.savetxt(f, results, fmt='%6.2f', delimiter=' '' ')
        
    return

CT()