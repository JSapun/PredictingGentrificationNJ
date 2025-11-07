# Predicting Neighborhood Gentrification in New Jersey

[**Final Research Paper (Bard College, 2024)**](https://github.com/JSapun/PredictingGentrificationNJ/blob/main/UndergraduateThesis.pdf)  
[**Website Landing Page**](https://jsapun.github.io/PredictingGentrificationNJ)

![Morris County Visual Change Prediction](https://github.com/JSapun/PredictingGentrificationNJ/blob/main/Figures/SemanticSegmentationExample.png)

---

## Overview
This repository contains all source code, data, and documentation for **Predicting Neighborhood Gentrification in New Jersey**, an undergraduate research thesis integrating computer vision, spatial analysis, and machine learning to detect early signs of gentrification.

The project combines **U.S. Census**, **Building Permit Survey**, **green space**, and **Google Street View** data to identify neighborhood-level changes.

Two models were developed:
- **K-Nearest Neighbors (KNN)** classifier to detect visual changes from Street View imagery  
- **K-Means** clustering algorithm to group neighborhoods by gentrification stage based on socio-economic and visual indicators

---

## Repository Structure

### `/Census`
Data cleaning and feature selection from 2022 Census estimates  
→ [`01_dataCleaning.ipynb`](Census/01_dataCleaning.ipynb)

### `/BPS`
Processing of 2024 Building Permit Survey data to extract development trends  
→ [`01_dataCleaning.ipynb`](BPS/01_dataCleaning.ipynb)

### `/GreenSpace`
Analysis of New Jersey park and green space data from Trust for Public Land  
→ [`02_morrisAnalysis.ipynb`](GreenSpace/02_morrisAnalysis.ipynb)

### `/manualTrainingSetSelection`
Python scripts for retrieving, labeling, and organizing Street View image pairs  
Includes a Tkinter GUI for manual classification

### `/SemanticSegmentation`
PyTorch implementation of ADE20K semantic segmentation for object detection  
→ [`02_test.py`](SemanticSegmentation/02_test.py)

### `/CompareVis`
Converts segmented images into numerical change metrics and merges with labels  
→ [`04_knnModel.ipynb`](CompareVis/04_knnModel.ipynb)

### `/PredictingGentrification`
Final clustering analysis integrating all processed datasets to predict gentrification risk  
→ [`01_clusteringModel.ipynb`](PredictingGentrification/01_clusteringModel.ipynb)

---

## Key Results
- **Region of Study:** Morris County, NJ  
- **Accuracy:** 71% (visual change classifier)  
- **Main Finding:** Northwest Morris County shows early-stage gentrification patterns, while Southeast regions exhibit established gentrification aligned with affordable housing investments  
- **Validation:** Results verified against official Morris County affordable housing data

---

## Citation
> Sapun, J. (2024). *Predicting Neighborhood Gentrification in New Jersey*. Bard College Undergraduate Thesis.

---

## License
This project is open-source and released under the MIT License.
