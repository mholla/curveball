"""
Calculating intrinsic curvature index and folding index for the gyral (concave/outward), 
sulcal(convex/inward) and saddle points of the cortex. 
introduced by Van Essen (1997) using Gaussian curvature, principal curvatures
and the sum of area of triangles meeting at each vertex.

Parameters:
----------

a: vertex-vise surface read from the {h}.pial.area.asc file
K: Gaussian curvature at each vertex read from the {h}.pial.K.asc file
k1: 1st principal curvature at each vertex read from the {h}.pial.k1.asc file
k2: 2nd principal curvature at each vertex read from the {h}.pial.k2.asc file
t: cortical thickness at each vertex read from the {h}.thickness.asc file

Returns:
-------
ICI: (Total) Intrinsic curvature index for convex, concave, and saddle points
FI: (Total) folding index for convex, concave, and saddle points
t: Mean cortical thickness for convex, concave, and saddle points
a: Total surface area for convex, concave, and saddle points

These are all saved in {h}.pial.ICI.FI.asc file for each hemisphere.

"""

def oppositeSigns(x, y): 
    return ((x * y) < 0)

def ICI_FI_area(subjects_dir,subject,hemi):
    
    import numpy as np
    import os

    a = '{h}.pial.area.asc'.format(h=hemi)
    K = '{h}.pial.K.asc'.format(h=hemi)
    k1 = '{h}.pial.k1.asc'.format(h=hemi)
    k2 = '{h}.pial.k2.asc'.format(h=hemi)
    t = '{h}.thickness.asc'.format(h=hemi)
    
    a = os.path.join(subjects_dir, subject, 'surf', a)
    K = os.path.join(subjects_dir, subject, 'surf', K)
    k1 = os.path.join(subjects_dir, subject, 'surf', k1)
    k2 = os.path.join(subjects_dir, subject, 'surf', k2)
    t = os.path.join(subjects_dir, subject, 'surf', t)
    
    # reading Gaussian curvature
    with open(K,'r') as K_file:
        K_lines = K_file.readlines()
        
    K = np.zeros(len(K_lines))
        
    for i in range(len(K_lines)):
        K_data = K_lines[i].split()
        K[i] = K_data[4]
        
    # reading k1-principal curvature
    with open(k1,'r') as k1_file:
        k1_lines = k1_file.readlines()
        
    k1 = np.zeros(len(k1_lines))
        
    for i in range(len(k1_lines)):
        k1_data = k1_lines[i].split()
        k1[i] = k1_data[4]
        
    # reading k2-principal curvature
    with open(k2,'r') as k2_file:
        k2_lines = k2_file.readlines()
        
    k2 = np.zeros(len(k2_lines))
        
    for i in range(len(k2_lines)):
        k2_data = k2_lines[i].split()
        k2[i] = k2_data[4]
        
    # reading area file
    with open(a,'r') as a_file:
        a_lines = a_file.readlines()
        
    a = np.zeros(len(a_lines))
        
    for i in range(len(a_lines)):
        a_data = a_lines[i].split()
        a[i] = a_data[4]
        
    # reading thickness
    with open(t,'r') as t_file:
        t_lines = t_file.readlines()
        
    t = np.zeros(len(t_lines))
        
    for i in range(len(t_lines)):
        t_data = t_lines[i].split()
        t[i] = t_data[4]
    
    # Positive Gaussian Curvature divided into sulci and gyral points by using principal curvatures
    
    K_gyr = np.zeros(len(K))
    K_sulc = np.zeros(len(K))
    K_saddle = np.zeros(len(K))
    
    a_gyr = np.zeros(len(a))
    a_sulc = np.zeros(len(a))
    a_saddle = np.zeros(len(a))
    
    t_gyr = np.zeros(len(t))
    t_sulc = np.zeros(len(t))
    t_saddle = np.zeros(len(t))
    
    k1_gyr = np.zeros(len(k1))
    k2_gyr = np.zeros(len(k2))
    
    k1_sulc = np.zeros(len(k1))
    k2_sulc = np.zeros(len(k2))
    
    k1_saddle = np.zeros(len(k1))
    k2_saddle = np.zeros(len(k2))
    
    for i in range(len(k1)):
        if k1[i] < 0 and k2[i] < 0:
            K_gyr[i] = K[i]
            a_gyr[i] = a[i]
            t_gyr[i] = t[i]
            k1_gyr[i] = k1[i]
            k2_gyr[i] = k2[i]
            
    for i in range(len(k1)):
        if k1[i] > 0 and k2[i] > 0:
            K_sulc[i] = K[i]
            a_sulc[i] = a[i]
            t_sulc[i] = t[i]
            k1_sulc[i] = k1[i]
            k2_sulc[i] = k2[i]
            
    for i in range(len(k1)):
        if (oppositeSigns(k1[i], k2[i]) == True):
            K_saddle[i] = K[i]
            a_saddle[i] = a[i]
            t_saddle[i] = t[i]
            k1_saddle[i] = k1[i]
            k2_saddle[i] = k2[i]
            
    for i in range(len(K_gyr)):
        if K_gyr[i] > 5:
            K_gyr[i] = 0
            a_gyr[i] = 0
            k1_gyr[i] = 0
            k2_gyr[i] = 0
            
    for i in range(len(K_sulc)):
        if K_sulc[i] > 5:
            K_sulc[i] = 0
            a_sulc[i] = 0
            k1_sulc[i] = 0
            k2_sulc[i] = 0
    
    ICI_gyr = np.sum(K_gyr*a_gyr/3)/4/np.pi    
    ICI_sulc = np.sum(K_sulc*a_sulc/3)/4/np.pi
    ICI_saddle = np.sum(K_saddle*a_saddle/3)/4/np.pi
    
    FI_gyr = np.sum(abs(k1_gyr) * abs(k1_gyr - k2_gyr) * a_gyr/3)/4/np.pi
    FI_sulc = np.sum(abs(k1_sulc) * abs(k1_sulc - k2_sulc) * a_sulc/3)/4/np.pi
    FI_saddle = np.sum(abs(k1_saddle) * abs(k1_saddle - k2_saddle) * a_saddle/3)/4/np.pi
    
    t_gyr = t_gyr[t_gyr != 0]
    t_sulc = t_sulc[t_sulc != 0]
    t_saddle = t_saddle[t_saddle != 0]
    
    a_gyr = a_gyr[a_gyr != 0]
    a_sulc = a_sulc[a_sulc != 0]
    a_saddle = a_saddle[a_saddle != 0]
    
    t_gyr = np.mean(t_gyr)
    t_sulc = np.mean(t_sulc)
    t_saddle = np.mean(t_saddle)
    
    a_gyr = sum(a_gyr)/3
    a_sulc = sum(a_sulc)/3
    a_saddle = sum(a_saddle)/3
    
    names = [('ICI_gyr', 'ICI_sulc', 'ICI_saddle', 'FI_gyr', 'FI_sulc', 'FI_saddle', 't_gyr', 't_sulc','t_saddle', 'a_gyr', 'a_sulc','a_saddle')]
    results = [(ICI_gyr, ICI_sulc, ICI_saddle, FI_gyr, FI_sulc, FI_saddle, t_gyr, t_sulc, t_saddle, a_gyr, a_sulc, a_saddle)]
    
    ICI_FI_name = '{h}.pial.ICI.FI.asc'.format(h=hemi)
    ICI_FI_name = os.path.join(subjects_dir, subject, 'surf', ICI_FI_name)
    
    np.savetxt(ICI_FI_name, names, fmt='%s', delimiter=' '' ') 
    
    with open(ICI_FI_name,'ab') as f:
        np.savetxt(f, results, fmt='%6.2f', delimiter=' '' ')
    
    return 
 
