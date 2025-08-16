import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_style('whitegrid')

def generate_eda_visuals(df: pd.DataFrame, save_path: str = "eda_outputs/"):
    os.makedirs(save_path, exist_ok=True)
    
    num_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    
    # Numerical distributions
    for col in num_cols:
        plt.figure(figsize=(8, 4))
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(f"Distribution of {col}")
        plt.savefig(os.path.join(save_path, f"distribution_{col}.png"))
        plt.close()
        
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=df[col].dropna())
        plt.title(f"Boxplot of {col}")
        plt.savefig(os.path.join(save_path, f"boxplot_{col}.png"))
        plt.close()
    
    # Categorical counts
    for col in cat_cols:
        plt.figure(figsize=(8, 4))
        sns.countplot(y=df[col])
        plt.title(f"Countplot of {col}")
        plt.savefig(os.path.join(save_path, f"countplot_{col}.png"))
        plt.close()
