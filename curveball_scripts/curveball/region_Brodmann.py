"""
Cortical regional surface data generated from Brodmann atlas per subject
"""

def region_Brodmann(subjects_dir, subject, x, y, z, a, b, c):
    
    import numpy as np
    import os
    
    hemis = ['lh']
    
    for hemi in hemis:

        label = ['BA1_exvivo', 'BA2_exvivo', 'BA3a_exvivo', 'BA3b_exvivo', 'BA4a_exvivo', 'BA4p_exvivo', 
                 'BA44_exvivo', 'BA45_exvivo', 'V1_exvivo', 'V2_exvivo', 'MT_exvivo', 'entorhinal_exvivo', 'perirhinal_exvivo']
        
        curv = ['SI', 'H', 'K', 'thickness', 'sulc', 'sulc.shrink']
        
        for i in range(len(label)):
            
            label_name = '{h}.{l}.label'.format(l=label[i], h=hemi) 
            label_path = os.path.join(subjects_dir, subject, 'label', label_name)
            
            # Read vertex indices from the label file
            with open(label_path,'r') as label_file:
                label_lines = label_file.readlines()
                
            label_data = np.zeros(len(label_lines)-2)
                
            for k in range(len(label_data)):
                input_label = label_lines[k+2].split()
                label_data[k] = input_label[0]
            
            # Read curvature (or thickness or depth) file
            for j in range(len(curv)):

                if curv[j] == 'thickness' or curv[j] == 'sulc' or curv[j] == 'sulc.shrink':
                    curv_name = '{h}.{c}.asc'.format(c=curv[j], h=hemi)
                else:
                    curv_name = '{h}.pial.{c}.asc'.format(c=curv[j], h=hemi)
                
                curv_name = os.path.join(subjects_dir, subject, 'surf', curv_name)
                
                with open(curv_name,'r') as curv_file:
                    curv_lines = curv_file.readlines() 
                curv_data = np.zeros(len(curv_lines))
                    
                for m in range(len(curv_lines)): 
                    input_curv = curv_lines[m].split()
                    curv_data[m] = float(input_curv[4])
        
                curv_label = np.zeros(len(curv_data))
                
                for h in label_data:
                    curv_label[int(h)] = curv_data[int(h)]
                   
                # Write results to text file             
                if curv[j] == 'thickness' or curv[j] == 'sulc' or curv[j] == 'sulc.shrink':
                    curv_name = '{h}.{c}.{l}.asc'.format(c=curv[j], l=label[i], h=hemi)
                else:
                    curv_name = '{h}.pial.{c}.{l}.asc'.format(c=curv[j], l=label[i], h=hemi)
                
                curv_name = os.path.join(subjects_dir, subject, 'surf', 'label_surf_BA', curv_name) # generate an empty folder named label_surf_Destrieux under surf 
                
                indices = np.array(range(len(curv_label)))
                columns = np.column_stack([x, y, z, curv_label])
                
                np.savetxt(curv_name, indices, fmt='%03d', delimiter=' '' ') 
                
                with open(curv_name,'r') as f:
                    lines = f.read().splitlines()
                with open(curv_name, 'w') as f: 
                    for n in range(len(columns)):
                        f.write('\n'.join([lines[n] + ' ' + '%10.6f' % (columns[n,0])  + ' ' + '%10.6f' % (columns[n,1])
                        + ' ' + '%10.6f' % (columns[n,2]) + ' ' + '%10.6f' % (columns[n,3])])+ '\n')  
                                    
        return
                     
