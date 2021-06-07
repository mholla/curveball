"""
Cortical regional surface data generated from Brodmann atlas per subject
"""

def label():
    
    import numpy as np
    import os
    import coords_nodes   
    
    input_txt = 'subjects_yale_TD.txt'
    path = os.path.join(os.getcwd(),input_txt)
    with open(path) as f: lines = f.read().splitlines()
    
    for line in lines:
        
        subjects_name = 'Yale_vtk'
        subjects_dir = os.path.join(os.getcwd(),subjects_name)
        subject = '{l}'.format(l=line)
        
        x,y,z,a,b,c = coords_nodes.coords_nodes(subjects_dir,subject)
    
        label = ['BA1_exvivo', 'BA2_exvivo', 'BA3a_exvivo', 'BA3b_exvivo', 'BA4a_exvivo', 'BA4p_exvivo', 
                 'BA44_exvivo', 'BA45_exvivo', 'V1_exvivo', 'V2_exvivo', 'MT_exvivo', 'entorhinal_exvivo', 'perirhinal_exvivo']
        
        curv = ['SI', 'H', 'K', 'thickness', 'sulc', 'sulc.shrink', 'SI.w2', 'H.w2', 'K.w2', 'thickness.w2']
        
        for i in range(len(label)):
            
            label_name = 'lh.{l}.label'.format(l=label[i]) 
            label_path = os.path.join(subjects_dir, subject, 'label', 'labels_lh', label_name)
            
            # Read vertex indices from the label file
            with open(label_path,'r') as label_file:
                label_lines = label_file.readlines()
                
            label_data = np.zeros(len(label_lines)-2)
                
            for k in range(len(label_data)):
                input_label = label_lines[k+2].split()
                label_data[k] = input_label[0]
            
            # Read curvature (or thickness or depth) file
            for j in range(len(curv)):

                if curv[j] == 'thickness' or curv[j] == 'sulc' or curv[j] == 'sulc_shrink' or curv[j] == 'thickness.w2':
                    curv_name = 'lh.{c}.asc'.format(c=curv[j])
                else:
                    curv_name = 'lh.pial.{c}.asc'.format(c=curv[j])
                
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
                if curv[j] == 'thickness' or curv[j] == 'sulc' or curv[j] == 'sulc_shrink' or curv[j] == 'thickness.w2':
                    curv_name = 'lh.{c}.{l}.asc'.format(c=curv[j], l=label[i])
                else:
                    curv_name = 'lh.pial.{c}.{l}.asc'.format(c=curv[j], l=label[i])
                
                curv_name = os.path.join(subjects_dir, subject, 'surf', 'label_surf_BA', curv_name)
                
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
                     
