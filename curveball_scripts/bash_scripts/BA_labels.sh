#!/bin/bash

export FREESURFER_HOME=/Applications/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export SUBJECTS_DIR=//Users/nagehan/Documents/scripts2/bigbrain/Yale_vtk

input="/Users/nagehan/subjects/subjects_yale_TD.txt"

while IFS= read -r line

do
	echo "$line"
	printf '%s\n' "$line"

	mris_convert $SUBJECTS_DIR/$line/surf/lh.pial.asc $SUBJECTS_DIR/$line/surf/lh.pial
	mris_convert $SUBJECTS_DIR/$line/surf/lh.white.asc $SUBJECTS_DIR/$line/surf/lh.white
	mris_smooth -n 3 -nw $SUBJECTS_DIR/$line/surf/lh.pial $SUBJECTS_DIR/$line/surf/lh.smoothwm
	mris_inflate -n 30 -dist 0.01 $SUBJECTS_DIR/$line/surf/lh.pial $SUBJECTS_DIR/$line/surf/lh.inflated
	mris_sphere $SUBJECTS_DIR/$line/surf/lh.inflated $SUBJECTS_DIR/$line/surf/lh.sphere
	mris_register -curv $SUBJECTS_DIR/$line/surf/lh.sphere $FREESURFER_HOME/average/lh.average.curvature.filled.buckner40.tif $SUBJECTS_DIR/$line/surf/lh.sphere.reg
	mri_label2label --trgsurf pial --srcsubject fsaverage --srclabel $SUBJECTS_DIR/fsaverage/label/lh.BA1_exvivo.label --trgsubject $line --trglabel $SUBJECTS_DIR/$line/label/lh.BA1_exvivo.label --hemi lh --regmethod surface
	mri_label2label --trgsurf pial --srcsubject fsaverage --srclabel $SUBJECTS_DIR/fsaverage/label/lh.BA2_exvivo.label --trgsubject $line --trglabel $SUBJECTS_DIR/$line/label/lh.BA2_exvivo.label --hemi lh --regmethod surface
	mri_label2label --trgsurf pial --srcsubject fsaverage --srclabel $SUBJECTS_DIR/fsaverage/label/lh.BA3a_exvivo.label --trgsubject $line --trglabel $SUBJECTS_DIR/$line/label/lh.BA3a_exvivo.label --hemi lh --regmethod surface
	mri_label2label --trgsurf pial --srcsubject fsaverage --srclabel $SUBJECTS_DIR/fsaverage/label/lh.BA3b_exvivo.label --trgsubject $line --trglabel $SUBJECTS_DIR/$line/label/lh.BA3b_exvivo.label --hemi lh --regmethod surface
	mri_label2label --trgsurf pial --srcsubject fsaverage --srclabel $SUBJECTS_DIR/fsaverage/label/lh.BA4a_exvivo.label --trgsubject $line --trglabel $SUBJECTS_DIR/$line/label/lh.BA4a_exvivo.label --hemi lh --regmethod surface
	mri_label2label --trgsurf pial --srcsubject fsaverage --srclabel $SUBJECTS_DIR/fsaverage/label/lh.BA4p_exvivo.label --trgsubject $line --trglabel $SUBJECTS_DIR/$line/label/lh.BA4p_exvivo.label --hemi lh --regmethod surface
	mri_label2label --trgsurf pial --srcsubject fsaverage --srclabel $SUBJECTS_DIR/fsaverage/label/lh.BA6_exvivo.label --trgsubject $line --trglabel $SUBJECTS_DIR/$line/label/lh.BA4p_exvivo.label --hemi lh --regmethod surface
	mri_label2label --trgsurf pial --srcsubject fsaverage --srclabel $SUBJECTS_DIR/fsaverage/label/lh.BA44_exvivo.label --trgsubject $line --trglabel $SUBJECTS_DIR/$line/label/lh.BA44_exvivo.label --hemi lh --regmethod surface
	mri_label2label --trgsurf pial --srcsubject fsaverage --srclabel $SUBJECTS_DIR/fsaverage/label/lh.BA45_exvivo.label --trgsubject $line --trglabel $SUBJECTS_DIR/$line/label/lh.BA45_exvivo.label --hemi lh --regmethod surface
	mri_label2label --trgsurf pial --srcsubject fsaverage --srclabel $SUBJECTS_DIR/fsaverage/label/lh.V1_exvivo.label --trgsubject $line --trglabel $SUBJECTS_DIR/$line/label/lh.V1_exvivo.label --hemi lh --regmethod surface
	mri_label2label --trgsurf pial --srcsubject fsaverage --srclabel $SUBJECTS_DIR/fsaverage/label/lh.V2_exvivo.label --trgsubject $line --trglabel $SUBJECTS_DIR/$line/label/lh.V2_exvivo.label --hemi lh --regmethod surface
	mri_label2label --trgsurf pial --srcsubject fsaverage --srclabel $SUBJECTS_DIR/fsaverage/label/lh.MT_exvivo.label --trgsubject $line --trglabel $SUBJECTS_DIR/$line/label/lh.MT_exvivo.label --hemi lh --regmethod surface
	mri_label2label --trgsurf pial --srcsubject fsaverage --srclabel $SUBJECTS_DIR/fsaverage/label/lh.perirhinal_exvivo.label --trgsubject $line --trglabel $SUBJECTS_DIR/$line/label/lh.perirhinal_exvivo.label --hemi lh --regmethod surface
	mri_label2label --trgsurf pial --srcsubject fsaverage --srclabel $SUBJECTS_DIR/fsaverage/label/lh.entorhinal_exvivo.label --trgsubject $line --trglabel $SUBJECTS_DIR/$line/label/lh.entorhinal_exvivo.label --hemi lh --regmethod surface

done < "$input"