#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main script of the pipeline. Run this only. Brief instructions are as follows:
    
mesh_pial_white: decimates and smoothens the pial and white triangular surface meshes
mesh_alpha: alpha surface is generated and saved as .ply from the pial surface
cort_thick: calculates the cortical thickness from smooth white and pial surface meshes, average thickness is taken.
sulcal_depth: sulcal depth is calculated using the alpha surface
coords_nodes: vertex coordinates (x,y,z) and triangle connectivity (a,b,c) of each mesh for each hemisphere
neighbor_info: neighbors of each vertex
Gaussian_curvature: calculates the Gaussian curvature surface area for each vertex
mean_curvature: calculates the mean curvature for each vertex
k1_k2_SI: calculates the principal curvatures (K1 and k2) and shape index (SI) for each vertex
ICI_FI_area: calculates the total normalized intrinsic curvature index, total folding index, and surface area for all convex, concave, and saddle shaped points
region_Brodmann: surface data are labelled and extracted for each region of the Brodmann atlas
region_Destrieux: surface data are labelled and extracted for each region of the Destrieux atlas
smooth: surface data are smoothed with two iterations
t_ratio: calculates cortical thickness ratio (tg/ts) for different coverage ratio

Parameters:
----------

Read subjects line-by-line from the user-defined `subjects.txt` file (one subject ID per line).
Each subject directory should exist under the `subjects_base_dir` (e.g., /path/to/your/subjects/<subject_id>/surf/ should contain input files like lh.pial.vtk).
"""

import sys
import os
import coords_nodes
import neighbor_info
import mesh_pial_white
import mesh_alpha
import Gaussian_curvature
import mean_curvature
import k1_k2_SI_CVD
import ICI_FI_area
import cort_thick
import sulcal_depth
import smooth
# import region_Destrieux
# import region_Brodmann
import t_ratio

def curveball(subject_dir=None, subject=None): # function name and optional inputs

    # checks if there are inputs for subject path
    if subject_dir is None or subject is None:
        print("No subject_dir provided, falling back to reading from file")
        subjects_base_dir = "/path/to/your/subjects_directory"  # Replace this with the full path to your directory containing subject folders (e.g., /home/user/data/subjects)
        input_txt = 'sample_subjects.txt'  # The text file listing subject IDs (one per line), located in subjects_base_dir
        path = os.path.join(subjects_base_dir, input_txt) # concatenates subjects_base_dir with input_txt
        
        # checks if path is valid
        if not os.path.isfile(path): 
            print(f"Error: Input file {path} does not exist. Please create 'subjects.txt' with subject IDs or provide subject_dir/subject as arguments.")
            sys.exit(1) # exits script
            
        # opens file as f (with ensures the file closes after block is run)
        with open(path) as f: 
            lines = f.read().splitlines() # reads the file as a single string and then splits the lines to create a string vector
        
        # loops through each element in string vector
        for line in lines:
            subject = line.strip() # removes leading and trailing whitespace characters (cleans up spaces, newlines, and tabs)
            if not subject:
                continue # if there is no subject name then the rest of the block is not run and the next line is examined
            subject_dir = os.path.join(subjects_base_dir, subject) # concatenates base path with subject for full directory
            print(f"Fallback processing: subject_dir={subject_dir}, subject={subject}")
            process_subject(subject_dir, subject) # calls process_subject
                  
    # if there are inputs only run that one subject and path
    else:
        print(f"Using passed arguments: subject_dir={subject_dir}, subject={subject}")
        process_subject(subject_dir, subject)

def process_subject(subject_dir, subject):
    # subject_dir is the full path to the subject's directory (e.g., /path/to/your/subjects_directory/Yale_0050551)
    # Assumes 'surf/' folder exists under subject_dir with input files like lh.pial.vtk, rh.white.vtk, etc.

    hemis = ['lh', 'rh']

    # Process each hemisphere
    for hemi in hemis:
        print(f"Processing: subject_dir={subject_dir}, subject={subject}, hemi={hemi}")
        try:
            # Step 1: Process pial and white meshes
            mesh_pial_white.mesh_pial_white(subject_dir, subject, hemi)
            
            # Step 2: Generate alpha surface
            mesh_alpha.mesh_alpha(subject_dir, subject, hemi)
            
            # Step 3: Calculate cortical thickness
            cort_thick.cort_thick(subject_dir, subject, hemi)
            
            # Step 4: Calculate sulcal depth
            sulcal_depth.sulcal_depth(subject_dir, subject, hemi)
            
            # Step 5: Extract coordinates and connectivity
            x, y, z, a, b, c = coords_nodes.coords_nodes(subject_dir, subject, hemi)
            
            # Step 6: Calculate neighbor information
            neighbor_info.neighbor_info(a, b, c, x, y, z, subject_dir, subject, hemi)
            
            # Step 7: Calculate Gaussian curvature
            Gaussian_curvature.Gaussian_curvature(x, y, z, subject_dir, subject, hemi)
            
            # Step 8: Calculate mean curvature
            mean_curvature.mean_curvature(x, y, z, subject_dir, subject, hemi)
            
            # Step 9: Calculate principal curvatures, shape index, and curvedness
            k1_k2_SI_CVD.k1_k2_SI_CVD(x, y, z, subject_dir, subject, hemi)
            
            # Step 10: Calculate intrinsic curvature index and folding index
            ICI_FI_area.ICI_FI_area(subject_dir, subject, hemi)
            
            # Step 11: Smooth surface measures
            smooth.smooth(subject_dir, subject, x, y, z, hemi)
            
            # Step 12: Process Destrieux atlas (commented out due to missing script)
            # region_Destrieux.region_Destrieux(subject_dir, subject, hemi)
            
            # Step 13: Process Brodmann atlas (commented out due to missing script)
            # region_Brodmann.region_Brodmann(subject_dir, subject, hemi)
            
            # Step 14: Calculate cortical thickness ratio
            t_ratio.t_ratio(subject_dir, subject, hemi)
            
            print(f"Successfully processed {subject_dir} for hemi={hemi}")
        except Exception as e:
            print(f"Error processing {subject_dir} for hemi={hemi}: {str(e)}")
            continue

if __name__ == "__main__":
    if len(sys.argv) > 1:
        subject_dir = sys.argv[1]
        subject = os.path.basename(subject_dir)
        print(f"Command-line argument detected: sys.argv={sys.argv}, subject_dir={subject_dir}, subject={subject}")
        curveball(subject_dir, subject)
    else:
        print("No command-line argument provided, using fallback")
        curveball()