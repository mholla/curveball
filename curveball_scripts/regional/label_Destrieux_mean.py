"""
Calculates regional mean thickness from Destireux atlas
"""

def label():
    
    import numpy as np
    import os
    import coords_nodes   
    
    input_txt = 'subjects_yale_TD.txt'
    path = os.path.join(os.getcwd(),input_txt)
    with open(path) as f: lines = f.read().splitlines()
    
    for line in lines:
        
        subjects_name = 'Yale'
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
                 'lh.S_temporal_transverse', 'lh.Unknown']
              
        label_mean = np.zeros(len(label))
        
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
            
            # Read thickness 
                
            curv_name = 'lh.thickness.asc'
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
                
            mean_curv = sum(curv_label)/np.count_nonzero(curv_label)
            
            for h in label_data:
                curv_label[int(h)] = mean_curv
                
            # Write results to text file             
            curv_name = 'lh.thickness.{l}.asc'.format( l=label[i])
            curv_name = os.path.join(subjects_dir, subject, 'surf', 'label_surf_Destrieux_mean', curv_name)
            
            indices = np.array(range(len(curv_label)))
            columns = np.column_stack([x, y, z, curv_label])
            
            np.savetxt(curv_name, indices, fmt='%03d', delimiter=' '' ') 
            
            with open(curv_name,'r') as f:
                lines = f.read().splitlines()
            with open(curv_name, 'w') as f: 
                for n in range(len(columns)):
                    f.write('\n'.join([lines[n] + ' ' + '%10.6f' % (columns[n,0])  + ' ' + '%10.6f' % (columns[n,1])
                    + ' ' + '%10.6f' % (columns[n,2]) + ' ' + '%10.6f' % (columns[n,3])])+ '\n')  
                                    
            # Calculate mean value for each region                                           
            label_mean[i] = sum(curv_label)/np.count_nonzero(curv_label)
            
        columns = np.column_stack([label, label_mean])
        
        import operator
        columns = sorted(columns, key = operator.itemgetter(1), reverse = True) # sort from highest thickness to lowest
        
        mean_name = 'lh.label.asc'
        mean_name = os.path.join(subjects_dir, subject, 'surf', mean_name)
    
        np.savetxt(mean_name, columns, fmt='%s', delimiter=' '' ') 

        return


# This code needs to be run inside the surf-ice, scripting, python tab
import os
import numpy as np

# select one subject
subjects_name = 'Yale'
subjects_dir = os.path.join(os.getcwd(),subjects_name)
subject = 'Yale_0050559'
mesh = os.path.join(subjects_dir, subject, 'surf', 'lh.pial.asc')

# reading regional label names from highest mean thickness to lowest mean thickness
reg = 'lh.label.asc'
reg = os.path.join(subjects_dir, subject, 'surf', reg)

with open(reg,'r') as reg_file:
    reg_lines = reg_file.readlines()
    
reg = np.zeros(len(reg_lines))
reg = reg.astype(str)
    
for i in range(len(reg_lines)):
    reg_data = reg_lines[i].split()
    reg[i] = reg_data[0]
    
# copy and paste reg array into regions below.
# Beginning of surf-ice painting code
# Surf-ice painting (paint each region depending on mean cortical thickness from highest to lowest)
import gl
import os
gl.resetdefaults()
gl.azimuthelevation(70, 15)
#load mesh
subjects_name = 'Yale'
subjects_dir = '/Users/nagehan/subjects'
subject = 'Yale_0050559'
mesh = os.path.join(subjects_dir, subject, 'surf', 'lh.pial.asc')
gl.meshload(mesh)
regions = ['lh.G_cingul-Post-dorsal', 'lh.G_temp_sup-Plan_polar',
       'lh.G_insular_short', 'lh.S_orbital_med-olfact', 'lh.G_precuneus',
       'lh.G_oc-temp_med-Parahip', 'lh.G_orbital', 'lh.G_front_sup',
       'lh.G_Ins_lg_and_S_cent_ins', 'lh.G_precentral',
       'lh.G_temp_sup-G_T_transv', 'lh.G_cingul-Post-ventral',
       'lh.G_and_S_transv_frontopol', 'lh.Unknown',
       'lh.G_temp_sup-Lateral', 'lh.Pole_temporal',
       'lh.S_circular_insula_ant', 'lh.G_pariet_inf-Angular',
       'lh.G_front_middle', 'lh.G_and_S_occipital_inf',
       'lh.G_occipital_middle', 'lh.G_oc-temp_lat-fusifor',
       'lh.G_and_S_cingul-Mid-Ant', 'lh.G_front_inf-Opercular',
       'lh.S_pericallosal', 'lh.G_rectus', 'lh.G_occipital_sup',
       'lh.G_and_S_cingul-Mid-Post', 'lh.G_oc-temp_med-Lingual',
       'lh.G_and_S_paracentral', 'lh.S_subparietal',
       'lh.G_front_inf-Triangul', 'lh.G_pariet_inf-Supramar',
       'lh.S_precentral-sup-part', 'lh.S_intrapariet_and_P_trans',
       'lh.G_parietal_sup', 'lh.G_and_S_subcentral',
       'lh.G_front_inf-Orbital', 'lh.Lat_Fis-post',
       'lh.S_orbital-H_Shaped', 'lh.S_oc-temp_med_and_Lingual',
       'lh.S_parieto_occipital', 'lh.G_temporal_middle',
       'lh.S_circular_insula_sup', 'lh.G_temporal_inf',
       'lh.S_circular_insula_inf', 'lh.G_and_S_cingul-Ant',
       'lh.S_calcarine', 'lh.S_precentral-inf-part',
       'lh.S_oc_sup_and_transversal', 'lh.S_front_middle',
       'lh.S_occipital_ant', 'lh.Pole_occipital', 'lh.S_central',
       'lh.G_subcallosal', 'lh.S_suborbital', 'lh.G_temp_sup-Plan_tempo',
       'lh.S_oc_middle_and_Lunatus', 'lh.S_postcentral',
       'lh.S_cingul-Marginalis', 'lh.S_temporal_sup',
       'lh.Lat_Fis-ant-Vertical', 'lh.S_front_sup', 'lh.G_postcentral',
       'lh.S_temporal_inf', 'lh.G_and_S_frontomargin',
       'lh.S_collat_transv_post', 'lh.G_cuneus',
       'lh.S_temporal_transverse', 'lh.S_oc-temp_lat', 'lh.S_front_inf',
       'lh.S_collat_transv_ant', 'lh.S_orbital_lateral',
       'lh.Lat_Fis-ant-Horizont', 'lh.S_interm_prim-Jensen']
for i in range(len(regions)):
    overlay = os.path.join(subjects_dir, subject, 'surf', 'label_surf_Destrieux_mean', 'lh.thickness.{l}.asc'.format(l=regions[i]))
    gl.overlayload(overlay)  
    gl.overlaycolorname(i+1, 'viridis{n}'.format(n=i))
    gl.overlayinvert(i+1,1)
    gl.overlayminmax(i+1,0,0)
    gl.overlayextreme(i+1,1)
    gl.colorbarvisible(0)
        
# End of surf-ice code

# Generating color lut files for surf-ice to paint 
from matplotlib import cm
import numpy as np

# if uniform colormap such as viridis
viridis = cm.get_cmap('viridis', 75)
 
cmap = viridis.colors*255

for i in range(len(cmap)):
    cmap[i][3] = 0
cmap = cmap.astype(int)
    
cmap_file = '/Applications/Surfice/surfice.app/Contents/Resources/lut/viridis_cmap'
np.savetxt(cmap_file, cmap, fmt='%s', delimiter='|')    
    
lut_data=['[FLT] \n', 'min=0 \n', 'max=0 \n', '[INT] \n', 'numnodes=1 \n','[BYT] \n','nodeintensity0=0 \n','[RGBA255] \n']
l = ('nodergba0=')   

with open(cmap_file,'r') as g:
    lines = g.read().splitlines()
                    
for i in range(len(cmap)):
    f = open('/Applications/Surfice/surfice.app/Contents/Resources/lut/viridis{n}.clut'.format(n=i),'w')
    f.writelines(lut_data)
    f.close()

for i in range(len(cmap)):
    f = open('/Applications/Surfice/surfice.app/Contents/Resources/lut/viridis{n}.clut'.format(n=i),'a')
    color = l + lines[i]
    f.writelines(color)
    f.close()


# spectral colormap for brain figures, for linear segmented colormap
from matplotlib import cm
import numpy as np

l = 13
spectral = cm.get_cmap('Spectral', l)

a = np.asarray(spectral(0))*255
b = np.asarray(spectral(1))*255
c = np.asarray(spectral(2))*255
d = np.asarray(spectral(3))*255
e = np.asarray(spectral(4))*255
f = np.asarray(spectral(5))*255
g = np.asarray(spectral(6))*255
h = np.asarray(spectral(7))*255
i = np.asarray(spectral(8))*255
j = np.asarray(spectral(9))*255
k = np.asarray(spectral(10))*255
l = np.asarray(spectral(11))*255
m = np.asarray(spectral(12))*255
n = np.asarray(spectral(13))*255

spect = np.vstack((a,b,c,d,e,f,g,h,i,j,k,l,m,n))

for i in range(len(spect)):
    spect[i][3] = 0
spect = spect.astype(int)

cmap_file = '/Applications/Surfice/surfice.app/Contents/Resources/lut/spectral_cmap'
np.savetxt(cmap_file, spect, fmt='%s', delimiter='|')    
    
lut_data=['[FLT] \n', 'min=0 \n', 'max=0 \n', '[INT] \n', 'numnodes=1 \n','[BYT] \n','nodeintensity0=255 \n','[RGBA255] \n']
l = ('nodergba0=')   

with open(cmap_file,'r') as g:
    lines = g.read().splitlines()
                    
for i in range(len(spect)):
    f = open('/Applications/Surfice/surfice.app/Contents/Resources/lut/spectral{n}.clut'.format(n=i),'w')
    f.writelines(lut_data)
    f.close()

for i in range(len(spect)):
    f = open('/Applications/Surfice/surfice.app/Contents/Resources/lut/spectral{n}.clut'.format(n=i),'a')
    color = l + lines[i]
    f.writelines(color)
    f.close()


    
    
    
    
    
    
    
