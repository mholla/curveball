"""
@author: Nagehan

Title: Mesh connectivity and vertex coordinates

Inputs: subjects directory, sunbject name

First, the code reads the input mesh file (lh.pial.asc), and 
the coordinates of the vertices, vertex ID, and connectivity of the mesh is obtained.

Outputs:

x: x-coordinate of each vertex 
y: y-coordinate of each vertex
z: z-coordinate of each vertex

a: vertex ID-1 for each triangular face
b: vertex ID-2 for each triangular face
c: vertex ID-3 for each triangular face

You can input your own data and skip this part if you wish

Input mesh file format (the format is the same with Freesurfer ?h.pial/white file format: 
    1st line: some introductory header starting with #...
    2nd line: total number of nodes (blank space) total number of triangular faces
    3rd until end of total number of nodes: xcoord ycoord zcoord 0
    Rest: vertex1 vertex2 vertex3 0: connectivity for each triangle
    
Current working directory must be set to the subjects directory.
Input mesh file can be .asc or .txt file format.

"""

def coords_nodes(subjects_dir,subject,hemi):
    
    import numpy as np
    import os
        
    input_mesh = '{h}.pial.asc'.format(h=hemi)
    
    m_filename = os.path.join(subjects_dir, subject, 'surf', input_mesh)
    
    with open(m_filename,'r') as coord_file:
        coord_lines = coord_file.readlines()
        v_f = coord_lines[1].split()
        v = int(v_f[0])
        f = int(v_f[1])
    
    # Coordinates x,y,z
    x = np.zeros(len(coord_lines) - f-2)
    y = np.zeros(len(coord_lines) - f-2)
    z = np.zeros(len(coord_lines) - f-2)
    
    
    for i in range(2, len(coord_lines) - f): 
    
        coord_data = coord_lines[i].split()
        
        x[i-2] = float(coord_data[0])
        y[i-2] = float(coord_data[1])
        z[i-2] = float(coord_data[2])
          
    # Triangle vertex connectivity a, b, c
    a = np.zeros(len(coord_lines) - len(x) -2)
    b = np.zeros(len(coord_lines) - len(x) -2)
    c = np.zeros(len(coord_lines) - len(x) -2)
        
    for i in range(v+2, len(coord_lines)):
        
        tri_data = coord_lines[i].split()
        
        a[i-v-2] = int(tri_data[0])
        b[i-v-2] = int(tri_data[1])
        c[i-v-2] = int(tri_data[2])
        
    return x,y,z,a,b,c

