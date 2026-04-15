# Interpretable facial dynamics as behavioral and perceptual traces of deepfakes.

This repository contains all the code for analysis and preprocessing associated with the manuscript:

## Repository Contents
All scripts related to the paper can be found in the `Paper` folder, organised across Python and R subfolders. The scripts follow the sequence of steps outlined in the manuscript:

1. **OpenFace Feature Extraction** (`Paper/Python/`): Scripts for extracting and processing facial Action Unit time series from video stimuli using OpenFace.
2. **NMF Fitting & Validation** (`Paper/R/Final Analysis/`): Code to fit Non-negative Matrix Factorisation (NMF) models to learn spatiotemporal structure from Action Unit time series, including validation of the decomposition.
3. **Classification** (`Paper/R/Final Analysis/`): Scripts for CMFTS feature extraction and supervised classification of real vs. deepfake videos.
4. **Human Perception Analysis** (`Paper/R/Human Analysis/`): Preprocessing and analysis of human observer data, including human-model correspondence analyses.
5. **Sensitivity checks** (`Paper/R/Sensitivity Checks/`): Supplementary analyses including emotion-stratified classification, valence classification, substate analysis, and movement analysis.
6. **Figures**: Figure 1 is generated in `Paper/Python/facial-expression-figures.ipynb`, Figure 2, 3, and 5 are generated in `Paper/Python/Final Analysis/`, Figure 4 is generated in `Paper/R/Human Analysis/`.

## Data Availability
Supporting data is available at: https://osf.io/76agj/overview?view_only=c73a947a070b43e1abafe3e35d2cb773
