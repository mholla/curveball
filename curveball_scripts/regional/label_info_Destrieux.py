"""
Cortical regional surface data generated from Destrieux atlas per subject
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
    
        label = ['lh.G_and_S_cingul-Ant', 'lh.G_and_S_cingul-Mid-Ant', 'lh.G_and_S_cingul-Mid-Post',\
                 'lh.G_and_S_frontomargin', 'lh.G_and_S_occipital_inf', 'lh.G_and_S_paracentral', 'lh.G_and_S_subcentral',\
                 'lh.G_and_S_transv_frontopol', 'lh.G_cingul-Post-dorsal', 'lh.G_cingul-Post-ventral', 'lh.G_cuneus',
                 'lh.G_front_inf-Opercular', 'lh.G_front_inf-Orbital', 'lh.G_front_inf-Triangul', 'lh.G_front_middle',\
                 'lh.G_front_sup', 'lh.G_Ins_lg_and_S_cent_ins', 'lh.G_insular_short', 'lh.G_oc-temp_lat-fusifor',\
                 'lh.G_oc-temp_med-Lingual', 'lh.G_oc-temp_med-Parahip', 'lh.G_occipital_middle', 'lh.G_occipital_sup',\
                 'lh.G_orbital', 'lh.G_pariet_inf-Angular', 'lh.G_pariet_inf-Supramar', 'lh.G_parietal_sup', 'lh.G_postcentral',
                 'lh.G_precentral', 'lh.G_precuneus','lh.G_rectus', 'lh.G_subcallosal', 'lh.G_temp_sup-G_T_transv', \
                 'lh.G_temp_sup-Lateral', 'lh.G_temp_sup-Plan_polar', 'lh.G_temp_sup-Plan_tempo', 'lh.G_temporal_inf',\
                 'lh.G_temporal_middle', 'lh.Lat_Fis-ant-Horizont', 'lh.Lat_Fis-ant-Vertical','lh.Lat_Fis-post', \
                 'lh.Pole_occipital', 'lh.Pole_temporal', 'lh.S_calcarine','lh.S_central','lh.S_cingul-Marginalis', \
                 'lh.S_circular_insula_ant', 'lh.S_circular_insula_inf', 'lh.S_circular_insula_sup', 'lh.S_collat_transv_ant',\
                 'lh.S_collat_transv_post', 'lh.S_front_inf', 'lh.S_front_middle', 'lh.S_front_sup', 'lh.S_interm_prim-Jensen',\
                 'lh.S_intrapariet_and_P_trans','lh.S_oc_middle_and_Lunatus', 'lh.S_oc_sup_and_transversal', 'lh.S_oc-temp_lat',\
                 'lh.S_oc-temp_med_and_Lingual', 'lh.S_occipital_ant', 'lh.S_orbital_lateral', 'lh.S_orbital_med-olfact',\
                 'lh.S_orbital-H_Shaped', 'lh.S_parieto_occipital', 'lh.S_pericallosal', 'lh.S_postcentral', 'lh.S_precentral-inf-part',\
                 'lh.S_precentral-sup-part', 'lh.S_suborbital', 'lh.S_subparietal', 'lh.S_temporal_inf', 'lh.S_temporal_sup',\
                 'lh.S_temporal_transverse']
             
        curv = ['SI', 'H', 'K', 'thickness', 'sulc', 'sulc.shrink', 'SI.w2', 'H.w2', 'K.w2', 'thickness.w2']
        
        for i in range(len(label)):
            
            label_name = '{l}.label'.format(l=label[i]) 
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
                
                curv_name = os.path.join(subjects_dir, subject, 'surf', 'label_surf_Destrieux', curv_name)
                
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
                     
