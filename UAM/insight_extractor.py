import os
import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
from typing import Optional

def identify_target_column(df: pd.DataFrame) -> Optional[str]:
    """
    Identify the target column if exists.
    Heuristic: column named 'target' or 'label', or last column if it has fewer unique values.
    """
    candidates = ['target', 'label']
    for col in candidates:
        if col in df.columns:
            return col

    # Heuristic: last column with fewer unique values than half rows
    last_col = df.columns[-1]
    if df[last_col].nunique() < df.shape[0] / 2:
        return last_col

    return None

def determine_problem_type(df: pd.DataFrame, target_col: Optional[str]) -> str:
    """
    Determine problem type based on target column.
    Returns one of ['classification', 'regression', 'clustering']
    """
    if target_col is None:
        return 'clustering'

    target = df[target_col]
    if pd.api.types.is_numeric_dtype(target):
        unique_vals = target.nunique()
        if unique_vals <= 20:
            return 'classification'
        else:
            return 'regression'
    else:
        return 'classification'

def extract_key_insights(df: pd.DataFrame, target_col: Optional[str], problem_type: str) -> dict:
    """
    Extract key insights including influential features, summary stats, and anomalies.
    """
    insights = {}

    # Dataset summary
    insights['dataset_summary'] = {
        'num_rows': df.shape[0],
        'num_columns': df.shape[1],
        'target_column': target_col,
        'problem_type': problem_type
    }

    # Feature types
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

    # Influential features
    if target_col and problem_type in ['classification', 'regression']:
        X = df.drop(columns=[target_col])

        # Exclude datetime columns from features
        X = X.drop(columns=[col for col in datetime_cols if col in X.columns], errors='ignore')
        y = df[target_col]

        # Encode categorical features for mutual info
        X_enc = pd.get_dummies(X, drop_first=True)

        if problem_type == 'classification':
            mi = mutual_info_classif(X_enc, y, discrete_features='auto', random_state=42)
        else:
            mi = mutual_info_regression(X_enc, y, random_state=42)

        mi_series = pd.Series(mi, index=X_enc.columns)
        top_features = mi_series.sort_values(ascending=False).head(10)
        insights['top_influential_features'] = top_features.to_dict()
    else:
        insights['top_influential_features'] = {}

    # Summary statistics for top features
    top_feats = list(insights['top_influential_features'].keys())
    summary_stats = {}
    for feat in top_feats:
        if feat in df.columns and feat not in df.select_dtypes(include=['datetime64']).columns:
            summary_stats[feat] = {
                'mean': df[feat].mean(),
                'median': df[feat].median(),
                'std': df[feat].std()
            }
    insights['summary_statistics_top_features'] = summary_stats

    # Distribution patterns and anomalies (simple outlier detection)
    anomalies = {}
    for col in numeric_cols:
        if col not in df.select_dtypes(include=['datetime64']).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))]
            anomalies[col] = len(outliers)
    insights['outliers_count'] = anomalies

    return insights

def generate_insight_report(insights: dict, output_path: str = "reports/insight_report.md"):
    """
    Generate a human-readable Markdown insight report.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Data Insight Report\n\n")

        ds = insights.get('dataset_summary', {})
        f.write("## Dataset Summary\n")
        f.write(f"- Number of rows: {ds.get('num_rows', 'N/A')}\n")
        f.write(f"- Number of columns: {ds.get('num_columns', 'N/A')}\n")
        f.write(f"- Target column: {ds.get('target_column', 'None')}\n")
        f.write(f"- Problem type: {ds.get('problem_type', 'N/A')}\n\n")

        f.write("## Top Influential Features\n")
        top_feats = insights.get('top_influential_features', {})
        if top_feats:
            for feat, score in top_feats.items():
                f.write(f"- {feat}: Mutual Information Score = {score:.4f}\n")
        else:
            f.write("No influential features identified or no target column.\n")
        f.write("\n")

        f.write("## Summary Statistics of Top Features\n")
        stats = insights.get('summary_statistics_top_features', {})
        if stats:
            for feat, stat in stats.items():
                f.write(f"- {feat}: Mean = {stat['mean']:.4f}, Median = {stat['median']:.4f}, Std = {stat['std']:.4f}\n")
        else:
            f.write("No summary statistics available.\n")
        f.write("\n")

        f.write("## Outlier Counts per Numeric Feature\n")
        outliers = insights.get('outliers_count', {})
        for feat, count in outliers.items():
            f.write(f"- {feat}: {count} outliers detected\n")
        f.write("\n")

        f.write("## Next Steps\n")
        if ds.get('problem_type') in ['classification', 'regression']:
            f.write("- Consider building predictive models using the identified influential features.\n")
        else:
            f.write("- Consider clustering or unsupervised learning techniques.\n")

    print(f"Insight report generated at: {output_path}")

def run_insight_extraction(df: pd.DataFrame, output_path: str = "reports/insight_report.md"):
    target_col = identify_target_column(df)
    problem_type = determine_problem_type(df, target_col)
    insights = extract_key_insights(df, target_col, problem_type)
    generate_insight_report(insights, output_path)
