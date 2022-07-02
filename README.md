# curveball

This pipeline includes many sub-scripts to quantitatively analyze the cortex of the brain. The pipeline can take any cortical (triangular) surface mesh as an input, including Freesurfer reconstructed surface mesh files such as ?h.pial and ?h.white. But convert them into .vtk format using mris_convert first. 

Data used for this pipeline (ABIDE dataset) can be obtained from http://fcon_1000.projects.nitrc.org/indi/abide/abide_I.html. The reconstructed surface files using Freesurfer are also in here: http://preprocessed-connectomes-project.org/abide/index.html

#Run bash scripts

First, run the mris_convert_vtk.sh script to convert ?h.pial and ?h.white files into ?h.pial.vtk and ?h.white.vtk files.

Secondly, run BA_labels.sh and Destrieux_labels.sh to generate the regional label files. If not interested in regional data, remove the region_Destrieux.py and
region_Brodmann.py from the curveball folder and skip this step.

#Run python scripts

The curveball.py script is the main script of the pipeline. Only run this script.

Generate an input text file with all the names of your subjects. An example is provided in the curveball folder. 
Put your subjects folder and input file inside the curveball folder together with all the other necessary scripts to successfully run the curveball.py. 

The pipeline takes approximately 1.5-2 hours to completely run for the decimated surface mesh (~40k nodes) per hemisphere using a single-core processor.

#Publications (if you use this tool in your research please also cite):

Demirci, Nagehan, and Maria A. Holland. “Cortical Thickness Systematically Varies with Curvature and Depth in Healthy Human Brains.” Human Brain Mapping. doi.org/10.1002/hbm.25776. 

Github link: https://github.com/mholla/HBM22




