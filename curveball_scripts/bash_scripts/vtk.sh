#!/bin/bash

export FREESURFER_HOME=/Applications/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export SUBJECTS_DIR=/Users/nagehan/subjects

input="/Users/nagehan/subjects/subjects_yale.txt"

while IFS= read -r line

do
	echo "$line"
	printf '%s\n' "$line"

	mris_convert $SUBJECTS_DIR/Yale/$line/surf/lh.white $SUBJECTS_DIR/Yale/$line/surf/lh.white.vtk
	mris_convert $SUBJECTS_DIR/Yale/$line/surf/rh.white $SUBJECTS_DIR/Yale/$line/surf/rh.white.vtk
		
	mris_convert $SUBJECTS_DIR/Yale/$line/surf/lh.pial $SUBJECTS_DIR/Yale/$line/surf/lh.pial.vtk
	mris_convert $SUBJECTS_DIR/Yale/$line/surf/rh.pial $SUBJECTS_DIR/Yale/$line/surf/rh.pial.vtk

	mris_convert $SUBJECTS_DIR/Yale/$line/surf/lh.inflated $SUBJECTS_DIR/Yale/$line/surf/lh.inflated.vtk
	mris_convert $SUBJECTS_DIR/Yale/$line/surf/rh.inflated $SUBJECTS_DIR/Yale/$line/surf/rh.inflated.vtk

done < "$input"
