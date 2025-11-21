# SEU Trajectory Analysis

**Developed as part of my Bachelor’s Thesis Project (2025).**  
Author: Offir Olivkovich  
Supervisor: Matan Yah Ben Zion  

---

## Overview

This repository contains the complete analysis pipeline used to extract, clean, and analyze trajectories from the SEU rolling-robot experiments.  
The project investigates whether simple mechanical configurations—mass placement, wheel orientation, and starting side—can encode directional behavior in a rolling robot **without onboard computation**.

The workflow includes:

- converting raw videos → per-frame trajectories  
- computing trial-level kinematic features  
- aggregating results across configurations  
- generating plots and summaries for flat and incline conditions  

All outputs are saved as structured CSV files to ensure reproducibility and enable downstream analysis.

---

## Repository Structure

```
seu-trajectory-analysis/
│
├── notebooks/
│   └── extract_trajectories_and_features.ipynb    # main analysis notebook
│
├── code/
│   ├── extract_trajectory.py       # video → trajectory extraction
│   ├── compute_features.py         # trial-level feature computation
│   └── estimate_kappa.py           # curvature estimation tools
│
├── data/
│   ├── videos/                     # raw videos (not included in repo)
│   │    ├── flat/
│   │    └── incline/
│   ├── trajectories/
│   │    └── all_trials.csv         # per-frame trajectory dataset
│   └── features/
│        └── features.csv           # trial-level feature summary
│
├── requirements.txt
└── README.md
```

---

## Pipeline Overview

### **1. Trajectory Extraction**

Videos are processed frame-by-frame to reconstruct the robot’s 2D motion.  
The resulting dataset (`data/trajectories/all_trials.csv`) includes:

- frame index  
- x, y coordinates  
- trial ID  
- condition (flat / incline)  
- mass position (front / back)  
- wheel orientation (normal / flipped) or starting side (left / right)

---

### **2. Feature Computation**

Each trial is summarized into quantitative kinematic features stored in  
`data/features/features.csv`.

Computed features include:

- **velocity**: mean, variability  
- **acceleration**: mean, variability  
- **startup acceleration**  
- **trajectory displacement**  
- **directional bias**  
- optional curvature estimation  
- full experimental metadata

---

### **3. Aggregation & Visualization**

The notebook also produces:

- `group_summary_flat` — aggregated statistics for flat trials  
- `group_summary_incline` — aggregated statistics for incline trials  

And generates:

- raw trajectory plots  
- grouped comparison views  
- feature distribution plots  
- incline behavior visualizations  

These outputs allow qualitative and quantitative comparison of the robot’s behavior under different mechanical configurations.

---

## Environment Setup

### **1. Create and activate a virtual environment**
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### **2. Install dependencies**
```bash
pip install -r requirements.txt
```

### **3. Launch Jupyter Lab**
```bash
python -m jupyter lab
```

Open the main analysis notebook:

```
notebooks/extract_trajectories_and_features.ipynb
```

---

## Output Files

### **Trajectory-level data**
`data/trajectories/all_trials.csv`  
Contains per-frame (x, y) positions + metadata.

### **Feature-level data**
`data/features/features.csv`  
Contains trial-level kinematic summaries.

### **Aggregated summaries**
Generated inside the notebook:

- `group_summary_flat`  
- `group_summary_incline`

### **Figures**
All trajectory and feature plots produced during analysis.

---

## Notes

- Raw videos are **not stored** in the repository due to size, but the folder structure is preserved.  
- The notebook is fully re-runnable once the videos are placed in `data/videos/flat` and `data/videos/incline`.  

---

