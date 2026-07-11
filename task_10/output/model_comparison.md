# Model Comparison

## Regression
Target: CO(GT), predicted from PT08 sensor readings and weather features.
Model RMSE: 0.6840, Baseline RMSE: 1.5060
Model R2: 0.7930, Baseline R2: -0.0036

## Classification
Target: high_co, 1 if CO(GT) is above the training median, else 0.
Model accuracy: 0.8905, Baseline accuracy: 0.4883
Model F1: 0.8893, Baseline F1: 0.0000

## Clustering
Features used: T, RH. Labels were not used during clustering.
Inertia: 5950.8414
Silhouette score: 0.3545
