# Exploratory Data Analysis Report

## Dataset Overview
- Number of rows: 7093
- Number of columns: 3

## Summary Statistics
### Numerical Features
|        |   count |         mean |    median |          std |       min |           max |    skew |   kurtosis |
|:-------|--------:|-------------:|----------:|-------------:|----------:|--------------:|--------:|-----------:|
| Close  |    7093 | 43.1151      | 9.2645    | 60.9995      | 0.069792  | 242.06        | 1.39392 |    0.62552 |
| Volume |    7093 |  1.34724e+08 | 9.936e+07 |  1.36989e+08 | 9.744e+06 |   2.08658e+09 | 4.7065  |   34.8444  |

### Categorical Features
|      |   unique_count |   mode_freq |   missing |
|:-----|---------------:|------------:|----------:|
| Date |           7093 |           1 |         0 |

## Key Insights
- Feature 'Close' has 147 potential outliers.
- Feature 'Volume' has 478 potential outliers.
- Features with high variance: Volume

## Visualizations
![correlation_heatmap.png](correlation_heatmap.png)
![dist_Close.png](dist_Close.png)
![dist_Volume.png](dist_Volume.png)
