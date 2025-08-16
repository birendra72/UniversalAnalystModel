import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis
from typing import List, Optional
from matplotlib.colors import LinearSegmentedColormap, to_hex
import re
import warnings
from matplotlib import font_manager

sns.set_style('whitegrid')

def generate_summary_statistics(df: pd.DataFrame) -> dict:
    summary = {}

    num_cols = df.select_dtypes(include=[np.number]).columns
    num_stats = df[num_cols].agg(['count', 'mean', 'median', 'std', 'min', 'max']).T
    num_stats['skew'] = df[num_cols].apply(skew)
    num_stats['kurtosis'] = df[num_cols].apply(kurtosis)
    summary['numerical'] = num_stats

    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    cat_stats = pd.DataFrame(index=cat_cols, columns=['unique_count', 'mode_freq', 'missing'])
    for col in cat_cols:
        unique_count = df[col].nunique(dropna=True)
        mode_freq = df[col].value_counts(dropna=True).max() if unique_count > 0 else 0
        missing = df[col].isnull().sum()
        cat_stats.loc[col] = [unique_count, mode_freq, missing]
    summary['categorical'] = cat_stats

    return summary

def extract_eda_insights(df: pd.DataFrame) -> List[str]:
    insights = []

    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))]
        if not outliers.empty:
            insights.append(f"Feature '{col}' has {len(outliers)} potential outliers.")

    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in cat_cols:
        counts = df[col].value_counts(normalize=True, dropna=True)
        if counts.iloc[0] > 0.9:
            insights.append(f"Categorical feature '{col}' is highly imbalanced (dominant class > 90%).")

    corr_matrix = df[num_cols].corr().abs()
    strong_corrs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            val = corr_matrix.iloc[i, j]
            if isinstance(val, (float, np.floating)) and val > 0.8:
                strong_corrs.append((corr_matrix.columns[i], corr_matrix.columns[j], val))
    if strong_corrs:
        for c1, c2, val in strong_corrs:
            insights.append(f"Features '{c1}' and '{c2}' have strong correlation: {val:.2f}")

    variances = df[num_cols].var()
    high_var = variances[variances > variances.quantile(0.75)].index.tolist()
    if high_var:
        insights.append(f"Features with high variance: {', '.join(high_var)}")

    datetime_cols = df.select_dtypes(include=['datetime64']).columns
    for col in datetime_cols:
        series = df[col].dropna()
        if series.empty:
            continue
        diffs = series.diff().dropna()
        min_diff = diffs.min()
        if isinstance(min_diff, pd.Timedelta) and min_diff >= pd.Timedelta(0):
            insights.append(f"Datetime feature '{col}' is monotonic increasing.")

    return insights

def generate_eda_visuals(df, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Identify column types
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    # Limit high-cardinality categoricals for plots
    low_card_cats = [col for col in categorical_cols if df[col].nunique() <= 20]

    # ----- 1. Correlation Heatmap -----
    if len(numeric_cols) >= 2:
        plt.figure(figsize=(8, 6))
        corr = df[numeric_cols].corr()
        sns.heatmap(corr, annot=False, cmap="coolwarm", center=0)
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "correlation_heatmap.png"))
        plt.close()

    # ----- 2. Key Numeric Distribution Plots -----
    for col in numeric_cols:
        plt.figure(figsize=(6, 4))
        sns.histplot(df[col].dropna(), kde=True, bins=30)
        plt.title(f"Distribution of {col}")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"dist_{col}.png"))
        plt.close()

    # ----- 3. Categorical Count Plots -----
    for col in low_card_cats:
        plt.figure(figsize=(6, 4))
        sns.countplot(x=df[col])
        plt.xticks(rotation=45)
        plt.title(f"Count of {col}")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"count_{col}.png"))
        plt.close()

    # ----- 4. Numeric vs Numeric (Top Correlated Pair) -----
    if len(numeric_cols) >= 2:
        corr_pairs = (
            df[numeric_cols]
            .corr()
            .unstack()
            .sort_values(ascending=False)
            .drop_duplicates()
        )
        corr_pairs = corr_pairs[(corr_pairs < 0.999) & (corr_pairs > 0.3)]
        if not corr_pairs.empty:
            top_pair = corr_pairs.index[0]
            plt.figure(figsize=(6, 4))
            sns.scatterplot(x=df[top_pair[0]], y=df[top_pair[1]], alpha=0.6)
            sns.regplot(x=df[top_pair[0]], y=df[top_pair[1]], scatter=False, color='red')
            plt.title(f"Relationship: {top_pair[0]} vs {top_pair[1]}")
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"scatter_{top_pair[0]}_{top_pair[1]}.png"))
            plt.close()

    # ----- 5. Numeric vs Categorical (Only Low-Cardinality) -----
    if numeric_cols and low_card_cats:
        for cat_col in low_card_cats:
            num_col = numeric_cols[0]  # First numeric for speed
            plt.figure(figsize=(6, 4))
            sns.boxplot(x=df[cat_col], y=df[num_col])
            plt.xticks(rotation=45)
            plt.title(f"{num_col} by {cat_col}")
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, f"box_{num_col}by{cat_col}.png"))
            plt.close()

    # ----- 6. Time-Series Plot (if datetime exists) -----
    datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()
    if datetime_cols and numeric_cols:
        date_col = datetime_cols[0]
        num_col = numeric_cols[0]
        plt.figure(figsize=(8, 4))
        df_sorted = df.sort_values(by=date_col)
        sns.lineplot(x=df_sorted[date_col], y=df_sorted[num_col])
        plt.title(f"Trend of {num_col} over {date_col}")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"trend_{num_col}over{date_col}.png"))
        plt.close()

    print(f"✅ EDA visuals saved in {output_dir}")

def generate_eda_report(df: pd.DataFrame, save_path: str = "eda_outputs/", problem_type: Optional[str] = None):
    os.makedirs(save_path, exist_ok=True)
    report_path = os.path.join(save_path, "eda_report.md")

    summary_stats = generate_summary_statistics(df)
    insights = extract_eda_insights(df)
    generate_eda_visuals(df, save_path)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Exploratory Data Analysis Report\n\n")
        f.write("## Dataset Overview\n")
        f.write(f"- Number of rows: {df.shape[0]}\n")
        f.write(f"- Number of columns: {df.shape[1]}\n\n")

        f.write("## Summary Statistics\n")
        f.write("### Numerical Features\n")
        f.write(summary_stats['numerical'].to_markdown() + "\n\n")

        f.write("### Categorical Features\n")
        f.write(summary_stats['categorical'].to_markdown() + "\n\n")

        f.write("## Key Insights\n")
        for insight in insights:
            f.write(f"- {insight}\n")
        f.write("\n")

        f.write("## Visualizations\n")
        for file in sorted(os.listdir(save_path)):
            if file.endswith(".png"):
                f.write(f"![{file}]({file})\n")

    print(f"EDA report generated at: {report_path}")

def check_existing_visualizations(save_path: str) -> bool:
    """Check if visualizations already exist in the given directory"""
    if not os.path.exists(save_path):
        return False
    
    expected_files = [
        "correlation_heatmap.png"
    ]
    
    # Check for at least some expected visualization files
    existing_files = [f for f in os.listdir(save_path) if f.endswith('.png')]
    return len(existing_files) > 0

def run_full_eda(df: pd.DataFrame, save_path: str = "eda_outputs/", problem_type: Optional[str] = None):
    print("Starting full EDA analysis...")
    generate_eda_report(df, save_path, problem_type)
    print("EDA analysis completed.")
