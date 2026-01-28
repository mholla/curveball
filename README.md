Curveball

Pipeline for quantitative analysis of cortical surface meshes from Freesurfer (?h.pial / ?h.white).

Computes:
- Cortical thickness
- Sulcal depth (standard + shrunken alpha surface)
- Mean & Gaussian curvature
- Principal curvatures (k1, k2), shape index (SI), curvedness (CVD)
- Intrinsic curvature index (ICI) & folding index (FI)
- Gyral/sulcal thickness ratio at multiple coverage levels

Originally built for datasets like ABIDE; now generalized, significantly faster, and easier to use.

Citation
If you use this pipeline in published work, please cite:
Demirci, N., & Holland, S. K. (2023). Cortical thickness systematically varies with curvature and depth in healthy human brains. Human Brain Mapping. DOI: 10.1002/hbm.25776

Improvements in v2.0 (2025 refresh)

~90% faster neighbor discovery
The previous bottleneck (neighbor_info.py) was completely rewritten:
- Old: O(V × T) complexity (nested loops scanning all triangles for every vertex)
- New: O(T + V × N) using upfront vertex-to-triangle mapping
- Result: neighbor finding now takes seconds instead of minutes on typical meshes (~40k–150k vertices)

Added curvedness (CVD)
New output {h}.pial.cvd.asc = √((k₁² + k₂²)/2) in the improved k1_k2_SI_CVD.py (replaces old k1_k2_SI.py).

Generalized & cleaned up
- No hard-coded paths — edit one line in curveball.py
- Better file checks, empty-array handling, safer math
- Clearer docstrings and comments

See CHANGELOG.md for full details.

Requirements

- Python 3.6+
- Install dependencies:
pip install -r requirements.txt
(numpy, scipy, pyvista, open3d)

Prerequisites (one-time per dataset)

1. Freesurfer outputs: surf/?h.pial, surf/?h.white (lh/rh)

2. Convert to .vtk (run once):
cd bash_scripts
./mris_convert_vtk.sh /path/to/your/subjects_dir

Optional (for regional stats with Brodmann/Destrieux):
./BA_labels.sh /path/to/subjects_dir
./Destrieux_labels.sh /path/to/subjects_dir
(Comment out region calls in curveball.py if skipping.)

Quick Start

1. Organize your data:
/your/base/folder/
├── Subject001/
│   └── surf/
│       ├── lh.pial.vtk
│       ├── rh.pial.vtk
│       ├── lh.white.vtk
│       └── ...
├── Subject002/
└── subjects.txt          # one subject folder name per line

2. Clone or update the repo:
git clone https://github.com/mholla/curveball.git
cd curveball

3. Edit one line in python_scripts/curveball.py:
subjects_base_dir = "/your/base/folder"   # ← change this

4. Run:
cd python_scripts
python curveball.py

Or single subject:
python curveball.py /your/base/folder/Subject001

Outputs go into each subject’s surf/ folder (.asc files for thickness, curvatures, sulc, ICI/FI, CVD, ratios, etc.).

Runtime Estimate
~20-25 minutes per hemisphere on a typical laptop (decimated ~40k vertex mesh).

Folder Structure

- bash_scripts/ — conversion & labeling helpers
- python_scripts/ — main pipeline (curveball.py calls everything)
- subjects.txt — your subject list (copy from sample_subjects.txt)

Questions or bugs → email with issue. 