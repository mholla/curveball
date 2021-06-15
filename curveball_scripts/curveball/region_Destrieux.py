"""
Cortical regional surface data generated from Destrieux atlas per subject
Important: this label data 
"""

def region_Destrieux(subjects_dir, subject, x, y, z, a, b, c):
    
    import numpy as np
    import os
    
    hemis = ['lh']
    
    for hemi in hemis:
    
        label = ['G_and_S_cingul-Ant', 'G_and_S_cingul-Mid-Ant', 'G_and_S_cingul-Mid-Post',\
                 'G_and_S_frontomargin', 'G_and_S_occipital_inf', 'G_and_S_paracentral', 'G_and_S_subcentral',\
                 'G_and_S_transv_frontopol', 'G_cingul-Post-dorsal', 'G_cingul-Post-ventral', 'G_cuneus',
                 'G_front_inf-Opercular', 'G_front_inf-Orbital', 'G_front_inf-Triangul', 'G_front_middle',\
                 'G_front_sup', 'G_Ins_lg_and_S_cent_ins', 'G_insular_short', 'G_oc-temp_lat-fusifor',\
                 'G_oc-temp_med-Lingual', 'G_oc-temp_med-Parahip', 'G_occipital_middle', 'G_occipital_sup',\
                 'G_orbital', 'G_pariet_inf-Angular', 'G_pariet_inf-Supramar', 'G_parietal_sup', 'G_postcentral',
                 'G_precentral', 'G_precuneus','G_rectus', 'G_subcallosal', 'G_temp_sup-G_T_transv', \
                 'G_temp_sup-Lateral', 'G_temp_sup-Plan_polar', 'G_temp_sup-Plan_tempo', 'G_temporal_inf',\
                 'G_temporal_middle', 'Lat_Fis-ant-Horizont', 'Lat_Fis-ant-Vertical','Lat_Fis-post', \
                 'Pole_occipital', 'Pole_temporal', 'S_calcarine','S_central','S_cingul-Marginalis', \
                 'S_circular_insula_ant', 'S_circular_insula_inf', 'S_circular_insula_sup', 'S_collat_transv_ant',\
                 'S_collat_transv_post', 'S_front_inf', 'S_front_middle', 'S_front_sup', 'S_interm_prim-Jensen',\
                 'S_intrapariet_and_P_trans','S_oc_middle_and_Lunatus', 'S_oc_sup_and_transversal', 'S_oc-temp_lat',\
                 'S_oc-temp_med_and_Lingual', 'S_occipital_ant', 'S_orbital_lateral', 'S_orbital_med-olfact',\
                 'S_orbital-H_Shaped', 'S_parieto_occipital', 'S_pericallosal', 'S_postcentral', 'S_precentral-inf-part',\
                 'S_precentral-sup-part', 'S_suborbital', 'S_subparietal', 'S_temporal_inf', 'S_temporal_sup',\
                 'S_temporal_transverse']
             
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
                
                curv_name = os.path.join(subjects_dir, subject, 'surf', 'label_surf_Destrieux', curv_name) # generate an empty folder named label_surf_Destrieux under surf 
                
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
                     
