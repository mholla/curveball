# curveball

This pipeline includes many sub-scripts to quantitatively analyze the cortex of the brain. Although the pipeline can take any cortical (triangular) surface mesh as an input, the scripts are optimized to work with Freesurfer outputted pial and white surface meshes. 

Data used for this pipeline (Yale subset of the ABIDE database) can be obtained from http://fcon_1000.projects.nitrc.org/indi/abide/abide_I.html; cortical surface meshes (?h.pial and ?h.white) can be reconstructed using Freesurfer.

#Run bash scripts

First, run the mris_convert_vtk.sh script to convert ?h.pial and ?h.white files into ?h.pial.vtk and ?h.white.vtk files.

Secondly, run BA_labels.sh and Destrieux_labels.sh to generate the regional label files.

#Run python scripts

The curveball.py script is the main script of the pipeline. 
Generate an input text file which should list the names of your subjects. An example is provided in the curveball folder. 
Place your subjects folder and input file inside the curveball folder together with all the other necessary scripts to successfully run the curveball.py. 




