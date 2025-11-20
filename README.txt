SEU TRAJECTORY ANALYSIS
---------------------------------
Author: Offir Olivkovich
Bachelor Thesis Project
Supervisor: Matan Yah Ben Zion
2025
---------------------------------

This project contains all code, data processing steps, and analysis used to
extract and analyze the trajectories of the SEU rolling robot prototype.

Project structure:

seu-trajectory-analysis
  notebooks
    extract_trajectories.ipynb   main analysis notebook
  code
    extract_trajectory.py        video-to-trajectory extraction
    compute_features.py          computation of trial-level features
    estimate_kappa.py            curvature estimation utilities
  data
    videos                       raw videos (not included in the repository)
      flat
      incline
    trajectories
      all_trials.csv             per-frame trajectories for all trials
    features
      features.csv               trial-level feature summaries
  requirements.txt
  README.txt


Pipeline overview:

1. Trajectory extraction
   Raw videos are processed to extract (x, y) positions for every frame.
   The output file "data/trajectories/all_trials.csv" contains:
     - frame index
     - x and y position
     - trial id
     - condition (flat or incline)
     - position of the mass (front or back)
     - wheel orientation (normal or flipped) or starting side

2. Feature computation
   Each trial is summarized using "summarize_all_trials" into numerical
   features describing motion behavior. The output file
   "data/features/features.csv" contains:
     - mean and standard deviation of velocity
     - mean and standard deviation of acceleration
     - startup acceleration
     - displacement
     - directional bias
     - optional curvature metrics
     - metadata (trial, condition, position, orientation)

3. Aggregation and visualization
   Trial-level features are grouped and summarized to produce:
     group_summary_flat
     group_summary_incline
   These tables describe how mechanical configurations affect the robot's
   motion.
   Additional visualizations include:
     - raw trajectory plots
     - grouped trajectory comparisons
     - feature distributions and comparisons


Environment setup:

1. Create and activate a virtual environment:
     python -m venv .venv
     .\.venv\Scripts\activate

2. Install dependencies:
     pip install -r requirements.txt

3. Launch Jupyter Lab:
     python -m jupyter lab
   Then open "notebooks/extract_trajectories.ipynb".


Outputs produced:

- data/trajectories/all_trials.csv
    per-frame positions for every trial

- data/features/features.csv
    trial-level summary statistics

- group_summary_flat
- group_summary_incline
    aggregated feature tables (created inside the notebook)

- multiple visualization plots created during analysis



