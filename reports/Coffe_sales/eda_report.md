# Exploratory Data Analysis Report

## Dataset Overview
- Number of rows: 3636
- Number of columns: 12

## Summary Statistics
### Numerical Features
|             |   count |     mean |   median |     std |   min |   max |       skew |   kurtosis |
|:------------|--------:|---------:|---------:|--------:|------:|------:|-----------:|-----------:|
| hour_of_day |    3636 | 14.1669  |    14    | 4.22775 |  6    |    22 |  0.131124  |  -1.12408  |
| money       |    3636 | 31.7469  |    32.82 | 4.91993 | 18.12 |    40 | -0.523038  |  -0.661143 |
| Weekdaysort |    3636 |  3.84791 |     4    | 1.97598 |  1    |     7 |  0.0809382 |  -1.22873  |
| Monthsort   |    3636 |  6.39466 |     6    | 3.48069 |  1    |    12 |  0.0437939 |  -1.37446  |

### Categorical Features
|             |   unique_count |   mode_freq |   missing |
|:------------|---------------:|------------:|----------:|
| cash_type   |              2 |        3547 |         0 |
| card        |           1316 |         129 |        89 |
| coffee_name |              8 |         824 |         0 |
| Time_of_Day |              3 |        1231 |         0 |
| Weekday     |              7 |         585 |         0 |
| Month_name  |             12 |         525 |         0 |

## Key Insights
- Categorical feature 'cash_type' is highly imbalanced (dominant class > 90%).
- Features with high variance: money
- Datetime feature 'date' is monotonic increasing.
- Datetime feature 'datetime' is monotonic increasing.

## Visualizations
![box_hour_of_daybyMonth_name.png](box_hour_of_daybyMonth_name.png)
![box_hour_of_daybyTime_of_Day.png](box_hour_of_daybyTime_of_Day.png)
![box_hour_of_daybyWeekday.png](box_hour_of_daybyWeekday.png)
![box_hour_of_daybycash_type.png](box_hour_of_daybycash_type.png)
![box_hour_of_daybycoffee_name.png](box_hour_of_daybycoffee_name.png)
![correlation_heatmap.png](correlation_heatmap.png)
![count_Month_name.png](count_Month_name.png)
![count_Time_of_Day.png](count_Time_of_Day.png)
![count_Weekday.png](count_Weekday.png)
![count_cash_type.png](count_cash_type.png)
![count_coffee_name.png](count_coffee_name.png)
![dist_Monthsort.png](dist_Monthsort.png)
![dist_Weekdaysort.png](dist_Weekdaysort.png)
![dist_hour_of_day.png](dist_hour_of_day.png)
![dist_money.png](dist_money.png)
![trend_hour_of_dayoverdate.png](trend_hour_of_dayoverdate.png)
