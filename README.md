# Adversarial Robustness of Structure-from-Motion Pipelines

## Research Question
Can adversarially perturbed input images silently corrupt 
3D reconstruction pipelines, and can a lightweight detector 
prevent this?

## Status
In progress — Phase 1 (attack implementation)

## Approach
1. FGSM-based perturbation of SfM inputs
2. Chamfer distance measurement of reconstruction degradation
3. Lightweight feature-based detector (no GPU required)
4. Evaluation on DTU benchmark dataset

## Stack
- Python (attack, detector, evaluation)
- OpenCV, Open3D (existing pipeline)

## Base Pipeline
The reconstruction/ folder contains a Structure-from-Motion 
pipeline built with OpenCV and Open3D that takes 5-10 images 
and outputs a .ply point cloud file.
