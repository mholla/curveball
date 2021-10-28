"""
Shape index distribution profile for all subjects

Parameters:
----------
    shape index: {h}.pial.SI.asc for each subject
    input_txt, subjects_name, output_folder: must be defined in the curveball_plots.py file
Returns:
-------
    Distribution profile along with statistical data
"""

def SI(input_txt, subjects_name, output_folder):
    
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    import os
    import statistics
    
    path = os.path.join(os.getcwd(),input_txt)
    with open(path) as f: lines = f.read().splitlines()
    
    SI_all = []
    
    for line in lines:
        
        hemis = ['lh','rh']
            
        for hemi in hemis:
        
            SI = '{h}.pial.SI.asc'.format(h=hemi)
            
            subjects_dir = os.path.join(os.getcwd(),subjects_name)
            subject = '{l}'.format(l=line)
            
            SI = os.path.join(subjects_dir, subject, 'surf', SI)
                
           # reading shape index
            with open(SI,'r') as SI_file:
                SI_lines = SI_file.readlines()
                
            SI = np.zeros(len(SI_lines))
                
            for i in range(len(SI_lines)):
                SI_data = SI_lines[i].split()
                SI[i] = SI_data[4]
            
            SI = SI[SI != 0]
            
            SI_all = np.append(SI_all, SI)
        
    plt.figure()
    ax=sns.kdeplot(-SI_all, color='#3E4A89', shade=True, bw_adjust=5)
    ax.set(xlim=(-1, 1))
    fname = os.path.join('/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots', output_folder, 'si_all.png')
    plt.savefig(fname, dpi = 500)
    
    #Statistics
    var = statistics.variance(SI_all)
    var = np.var(SI_all)
    std = np.std(SI_all)
    mean = np.mean(SI_all)
    
    names = [('SI_mean', 'SI_std', 'SI_var')]
    results = [(mean, std, var)]
        
    SI_name = os.path.join('/afs/crc.nd.edu/group/commandlab/Nagehan/curveball_scripts/plots', output_folder, 'si_all.asc')
        
    np.savetxt(SI_name, names, fmt='%s', delimiter=' '' ') 
        
    with open(SI_name,'ab') as f:
        np.savetxt(f, results, fmt='%6.2f', delimiter=' '' ')
    
    return

