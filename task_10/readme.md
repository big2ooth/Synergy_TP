# Air Quality Machine Learning Pipeline

## Overview

This project builds a complete machine learning pipeline from scratch using NumPy and Pandas. The pipeline works on the Air Quality UCI dataset and includes data preprocessing, linear regression, logistic regression and K-Means clustering.

No machine learning libraries such as scikit-learn were used for implementing the models.

## Features

- Data cleaning and preprocessing
- Missing value handling
- Train, validation and test split
- Median imputation using training data
- Feature standardization
- Linear Regression using Gradient Descent
- Logistic Regression using Gradient Descent
- K-Means Clustering
- Model evaluation using common metrics
- Automatic generation of plots and output files


## Requirements

- Python 3.10 or newer
- NumPy
- Pandas
- Matplotlib

Install the required packages with:

```bash
pip install numpy pandas matplotlib
```

## Running the Project

Run the pipeline using:

```bash
python task_10/src/main.py task_10/data/AirQualityUCI.csv task_10/output
```

All results, plots and evaluation files will be saved inside the `output` folder.

## Models

### Linear Regression

Predicts CO(GT) using sensor readings and weather features.

Evaluation metrics:

- MAE
- MSE
- RMSE
- R² Score

### Logistic Regression

Classifies whether CO(GT) is above the median value.

Evaluation metrics:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

### K-Means Clustering

Clusters the data using Temperature and Relative Humidity.

Evaluation metrics:

- Inertia
- Silhouette Score

## Output

The project generates:

- Prediction CSV files
- Evaluation metrics
- Training loss curves
- Confusion matrix
- Actual vs predicted plot
- Cluster visualization
- Model comparison report
- Error analysis report
