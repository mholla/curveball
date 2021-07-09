"""
Mean curvature distribution profile for all subjects
"""
def H():
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    import os
    
    input_txt = 'subjects_ABIDE_TD.txt'
    path = os.path.join(os.getcwd(),input_txt)
    with open(path) as f: lines = f.read().splitlines()
    
    H_all = []
    
    for line in lines:
        
        hemis = ['lh','rh']
            
        for hemi in hemis:
        
            H = '{h}.pial.H.asc'.format(h=hemi)
            
            subjects_name = 'subjects_ABIDE_TD'
            subjects_dir = os.path.join(os.getcwd(),subjects_name)
            subject = '{l}'.format(l=line)
            
            H = os.path.join(subjects_dir, subject, 'surf', H)
                
           # reading mean curvature
            with open(H,'r') as H_file:
                H_lines = H_file.readlines()
                
            H = np.zeros(len(H_lines))
                
            for i in range(len(H_lines)):
                H_data = H_lines[i].split()
                H[i] = H_data[4]
            
            H[H < -1] = 0
            H[H > 1] = 0
            
            H = H[H != 0]
            
            H_all = np.append(H_all, H)
        
    plt.figure()
    ax=sns.kdeplot(H_all, color='#3E4A89', shade=True, bw_adjust=5)
    ax.set(xlim=(-1, 1))
    fname = '/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots/results_all/H.png'
    plt.savefig(fname, dpi = 500)
    
    #Statistics
    var = np.var(H_all)
    mean = np.mean(H_all)
    std = np.std(H_all)
    
    names = [('H_mean', 'H_std', 'H_var')]
    results = [(mean, std, var)]
        
    H_name = '/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots/results_all/H_all.asc'
        
    np.savetxt(H_name, names, fmt='%s', delimiter=' '' ') 
        
    with open(H_name,'ab') as f:
        np.savetxt(f, results, fmt='%6.2f', delimiter=' '' ')
    
    return






