"""
Gaussian curvature distribution profile for all subjects
"""
def K():
    
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    import os
    
    input_txt = 'subjects_ABIDE_TD.txt'
    path = os.path.join(os.getcwd(),input_txt)
    with open(path) as f: lines = f.read().splitlines()
    
    K_all = []
    
    for line in lines:
        
        hemis = ['lh','rh']
            
        for hemi in hemis:
        
            K = 'lh.pial.K.asc'
            
            subjects_name = 'subjects_ABIDE_TD'
            subjects_dir = os.path.join(os.getcwd(),subjects_name)
            subject = '{l}'.format(l=line)
            
            K = os.path.join(subjects_dir, subject, 'surf', K)
                
           # read Gaussian curvature
            with open(K,'r') as K_file:
                K_lines = K_file.readlines()
                
            K = np.zeros(len(K_lines))
                
            for i in range(len(K_lines)):
                K_data = K_lines[i].split()
                K[i] = K_data[4]
            
            K[K < -0.1] = 0
            K[K > 0.1] = 0
            
            K = K[K != 0]
            K_all = np.append(K_all, K)
        
    plt.figure()
    ax = sns.kdeplot(K_all, color='#3E4A89', shade=True, bw_adjust=5)
    ax.set(xlim=(-0.1, 0.1))
    fname = '/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots/results_all/K.png'
    plt.savefig(fname, dpi = 500)
    
    #Statistics
    var = np.var(K_all)
    std = np.std(K_all)
    mean = np.mean(K_all)
    
    names = [('K_mean', 'K_std', 'K_var')]
    results = [(mean, std, var)]
        
    K_name = '/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots/results_all/K_all.asc'
        
    np.savetxt(K_name, names, fmt='%s', delimiter=' '' ') 
        
    with open(K_name,'ab') as f:
        np.savetxt(f, results, fmt='%6.2f', delimiter=' '' ')
        
    return
    
