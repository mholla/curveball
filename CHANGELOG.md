# CHANGELOG

## v2.0 - Curvedness addition and Major Optimization - June 2026

This release delivers two improvements: a dramatic speedup of the slowest script in the pipeline (`neighbor_info.py`) and the addition of curvedness (CVD) computation. Minor fixes improve portability, robustness, and clarity for new users.

### Major Changes

- **neighbor_info.py – Massive Performance Optimization**  
  Original version was the slowest part of the entire pipeline due to nested loops scanning all triangles for every vertex → O(V × T) time complexity (V = vertices, T = triangles).  
  **New version reduces complexity to O(T + V × N)** (N ≈ average triangles per vertex, typically ~6).  
  - Built a **vertex-to-triangle mapping** upfront in O(T) time (list of triangles per vertex).  
  - Finding first two neighbors: now uses only the relevant triangles per vertex (no full scan).  
  - Finding remaining neighbors in circular order: checks only triangles connected to the vertex.  
  - Logic fully preserved: initializes `ndl`, finds initial neighbors, walks cycle, cleans up remaining entries when cycle closes.  
  Result: significantly faster neighbor discovery on typical cortical meshes (~40k–150k vertices).

- **Curvedness (CVD) Calculation – New Feature**  
  New script `k1_k2_SI_CVD.py` (replaces old `k1_k2_SI.py`):  
  - Computes **curvedness** = √((k₁² + k₂²)/2) and saves to `{h}.pial.cvd.asc`.  
  - Improved stability: clamps negative sqrt terms to 0, uses `atan2` for shape index.  
  - Added file existence checks and better error messages.

### Minor Changes & Cleanups

- **Path handling**: All scripts now use `os.path.join(subjects_dir, 'surf', ...)` consistently. Removed redundant `subject` argument from paths.
- **Robustness**: Added `try-except` for missing files, handled empty arrays (`np.mean` with fallback to 0), avoided division by zero in ratios, capped extreme curvature values.
- **curveball.py**: Generalized with editable `subjects_base_dir` placeholder, uses `subjects.txt`, supports single-subject CLI runs, commented out optional region atlas calls.
- **Other scripts**: Completed truncated code (e.g. `sulcal_depth.py` centering/shrinkage), improved docstrings/comments, minor efficiency tweaks.
- **Repo files**: updated README with clearer setup instructions.

## v1.0 – Original Release (2021)
- Initial pipeline focused on ABIDE dataset analysis: core curvature, thickness, sulcal depth, ICI/FI calculations.