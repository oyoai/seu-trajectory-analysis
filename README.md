# **SEU Trajectory Analysis**

### *Bachelor Thesis Project — 2025*

**Author:** Offir Olivkovich

**Supervisor:** Matan Yah Ben Zion

---

## Background

This repository documents one of several prototypes developed as part of a broader research effort investigating curvity (κ)—a geometric property introduced in the work of Matan Yah Ben Zion. Curvity quantifies how quickly a body turns when a force is applied, that is, the rate at which the heading angle changes in response to an external force. Differences in an individual robot’s curvity can accumulate at the swarm level, causing large-scale shifts in collective behavior (see [Casiulis et al., 2024](...)). Remarkably, all of these effects emerge without any active control.

The SEU (Scaled Evaluation Unit) is a prototype developed to reproduce the curvity-driven behaviors seen in vibration-based robots (see [Ben Zion et al. (2023) ](...)), adapting them to a rolling locomotion framework.

<div align="center">
  <img src="/mnt/Media/seu.png" 
       alt="SEU Rolling Robot" 
       width="430">
  <br>
  <em>Figure 1 — SEU rolling robot prototype</em>
</div>

To study how curvity-based behavior manifests in a real prototype, the SEU robot was filmed across two environments: a flat surface (control), and an inclined surface (with gravity acting as the force).

The goal of this analysis is to:

* extract accurate, per-frame trajectories from the raw videos
* compute kinematic features (velocity, acceleration, displacement, directional bias)
* compare configurations to evaluate whether mass placement produces **consistent, engineered behavior**
* create a clean, reproducible analysis pipeline for future curvature-based rolling robot studies

---

## Project Structure

```
seu-trajectory-analysis/
│
├── Code/                         # helper modules for tracking & feature extraction
│   ├── extract_trajectory.py
│   ├── compute_features.py
│   └── estimate_kappa.py
│
├── Data/
│   ├── Trajectories/             # exported per-frame trajectories (CSV)
│   └── Features/                 # trial-level feature tables (CSV)
│
├── Notebooks/
│   └── extract_trajectories_and_features.ipynb  # first analysis notebook
│   └── first_trial_kappa.ipynb                  # second analysis notebook
│
├── Media/                        # images (e.g., SEU model photo)
│
├── README.md
└── requirements.txt
```

> **Note:**
> Raw video recordings are excluded from the repository because they exceed practical storage limits.

---

## How to Explore This Repository

This repository is not intended as an install-and-run software package.
Its purpose is to document the processing pipeline, analysis logic, and intermediate datasets used in the SEU trajectory analysis component of my bachelor’s thesis.

If you are viewing this repository, the most important materials are:

## Notebooks:

### 1. [`extract_trajectories_and_features.ipynb`](Notebooks/extract_trajectories_and_features.ipynb)
The main analysis notebook. It contains the full trajectory extraction pipeline, feature computation, visualizations of all flat and incline configurations and full documentation of this process. The resulting datasets are used for downstream analysis.

### 2. [`calculate_curvity.ipynb`](Notebooks/calculate_curvity.ipynb)
This notebook performs the curvity-related analysis, connecting the extracted trajectories to the theoretical framework from Matan Yah Ben Zion’s research.

## Scripts:

### 1. [`extract_trajectory.py`](Code/extract_trajectory.py)  
Converts raw videos into per-frame trajectories using frame differencing and bounding-box tracking.

### 2. [`compute_features.py`](Code/compute_features.py)  
Computes trial-level kinematic metrics (velocity, acceleration, displacement, directional bias).

### 3. [`estimate_kappa.py`](Code/estimate_kappa.py)  
Utilities for curvature estimation and curvity related analysis.


## Output Data
The cleaned, structured datasets produced and used throughout the analysis.

### 1. [`all_trials.csv`](Data/Trajectories/all_trials.csv)  
Per-frame reconstructed trajectories for every trial.

### 2. [`features.csv`](Data/Features/features.csv)  
Trial-level summary metrics derived from the trajectories.

---




>#### Purpose of This Repository
> <em>This repository documents how the dataset used in the thesis was generated, provides reproducible code for verification, serves as a companion to the written thesis, and illustrates SEU’s behavior across different configurations.  
> It is <strong>not</strong> intended as a pip-installable package or general-purpose library.</em>

