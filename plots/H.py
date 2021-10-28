"""
Mean curvature distribution profile for all subjects

Parameters:
----------
    mean curvature: {h}.pial.H.asc for each subject
    input_txt, subjects_name, output_folder: must be defined in the curveball_plots.py file
Returns:
-------
    Distribution profile of mean curvature along with statistical data
"""

def H(input_txt, subjects_name, output_folder):
    
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    import os
    
    path = os.path.join(os.getcwd(),input_txt)
    with open(path) as f: lines = f.read().splitlines()
    
    H_all = []
    
    for line in lines:
        
        hemis = ['lh','rh']
            
        for hemi in hemis:
        
            H = '{h}.pial.H.asc'.format(h=hemi)
            
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
    fname = os.path.join('/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots', output_folder, 'H_all.png')
    plt.savefig(fname, dpi = 500)
    
    #Statistics
    var = np.var(H_all)
    mean = np.mean(H_all)
    std = np.std(H_all)
    
    names = [('H_mean', 'H_std', 'H_var')]
    results = [(mean, std, var)]
        
    H_name = os.path.join('/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots', output_folder, 'H_all.asc')
        
    np.savetxt(H_name, names, fmt='%s', delimiter=' '' ') 
        
    with open(H_name,'ab') as f:
        np.savetxt(f, results, fmt='%6.2f', delimiter=' '' ')
    
    return






