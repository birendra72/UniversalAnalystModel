import os
import pandas as pd
import numpy as np
import joblib
from typing import Optional
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from UAM import insight_extractor

def detect_target_column(df: pd.DataFrame, provided_target: Optional[str] = None) -> Optional[str]:
    if provided_target and provided_target in df.columns:
        return provided_target
    # Fallback to heuristic from insight_extractor
     
    return insight_extractor.identify_target_column(df)
def determine_problem_type(df: pd.DataFrame, target_col: str) -> str:
    return insight_extractor.determine_problem_type(df, target_col)

def preprocess_for_modeling(df: pd.DataFrame, target_col: str):
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Handle datetime columns
    datetime_cols = X.select_dtypes(include=['datetime64']).columns.tolist()
    if datetime_cols:
        X = pd.get_dummies(X, columns=datetime_cols)
        
    # Encode categorical features
    cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    if cat_cols:
        ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        X_cat = ohe.fit_transform(X[cat_cols])
        X_cat_df = pd.DataFrame(X_cat, columns=ohe.get_feature_names_out(cat_cols), index=X.index)
        X = X.drop(columns=cat_cols)
        X = pd.concat([X, X_cat_df], axis=1)

    # Encode target if classification and categorical
    if y.dtype == 'object' or str(y.dtype).startswith('category'):
        le = LabelEncoder()
        y = le.fit_transform(y)
    return X, y

def train_models(X_train, y_train, problem_type: str):
    models = {}
    if problem_type == 'classification':
        models['LogisticRegression'] = LogisticRegression(max_iter=1000)
        models['RandomForestClassifier'] = RandomForestClassifier()
        models['SVC'] = SVC(probability=True)
    else:
        models['LinearRegression'] = LinearRegression()
        models['RandomForestRegressor'] = RandomForestRegressor()
        models['SVR'] = SVR()

    trained_models = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        trained_models[name] = model
    return trained_models

def evaluate_models(models: dict, X_test, y_test, problem_type: str):
    results = {}
    for name, model in models.items():
        y_pred = model.predict(X_test)
        if problem_type == 'classification':
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
            cm = confusion_matrix(y_test, y_pred)
            results[name] = {
                'accuracy': acc,
                'precision': prec,
                'recall': rec,
                'f1_score': f1,
                'confusion_matrix': cm
            }
        else:
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            results[name] = {
                'rmse': rmse,
                'mae': mae,
                'r2_score': r2
            }
    return results
# save_path = os.path.join("reports", dataset_name) if dataset_name else "reports/"
def save_models(models: dict, model_dir: str = "models"):
    os.makedirs(model_dir, exist_ok=True)
    for name, model in models.items():
        path = os.path.join(model_dir, f"{name}.pkl")
        joblib.dump(model, path)

def plot_confusion_matrix(cm, classes, title='Confusion matrix', cmap='Blues', save_path=None):
    plt.figure(figsize=(6,6))
    sns.heatmap(cm, annot=True, fmt='d', cmap=cmap, xticklabels=classes, yticklabels=classes)
    plt.title(title)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.close()

def plot_actual_vs_predicted(y_test, y_pred, save_path=None):
    plt.figure(figsize=(6,6))
    plt.scatter(y_test, y_pred, alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title('Actual vs Predicted')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.close()

def plot_feature_importance(model, feature_names, save_path=None):
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        plt.figure(figsize=(8,6))
        sns.barplot(x=importances[indices], y=np.array(feature_names)[indices])
        plt.title('Feature Importances')
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        plt.close()

def run_modeling(df: pd.DataFrame, provided_target: Optional[str] = None, output_dir: str = "reports", model_dir: str = "models"):
    target_col = detect_target_column(df, provided_target)
    if not target_col:
        print("No target column detected. Skipping modeling step.")
        return

    problem_type = determine_problem_type(df, target_col)
    print(f"Detected problem type: {problem_type} with target column: {target_col}")

    X, y = preprocess_for_modeling(df, target_col)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = train_models(X_train, y_train, problem_type)
    results = evaluate_models(models, X_test, y_test, problem_type)
    save_models(models, model_dir)

    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "model_report.md")
    with open(report_path, 'w') as f:
        f.write("# Model Evaluation Report\n\n")
        f.write(f"Problem type: {problem_type}\n\n")
        for name, metrics in results.items():
            f.write(f"## {name}\n")
            for metric, value in metrics.items():
                if metric == 'confusion_matrix':
                    cm_path = os.path.join(output_dir, f"{name}_confusion_matrix.png")
                    plot_confusion_matrix(value, classes=np.unique(y), save_path=cm_path)
                    f.write(f"![Confusion Matrix]({f"{name}_confusion_matrix.png"})\n\n")
                else:
                    f.write(f"- {metric}: {value:.4f}\n")
            # Feature importance plot for tree-based models
            if problem_type in ['classification', 'regression'] and hasattr(models[name], 'feature_importances_'):
                fi_path = os.path.join(output_dir, f"{name}_feature_importance.png")
                plot_feature_importance(models[name], X.columns, save_path=fi_path)
                f.write(f"![Feature Importance]({f"{name}_feature_importance.png"})\n\n")
        # Actual vs Predicted plot for regression
        if problem_type == 'regression':
            y_pred = models['LinearRegression'].predict(X_test)
            avp_path = os.path.join(output_dir, "actual_vs_predicted.png")
            plot_actual_vs_predicted(y_test, y_pred, save_path=avp_path)
            f.write(f"![Actual vs Predicted]({"actual_vs_predicted.png"})\n\n")

    print(f"Modeling and evaluation report saved to {report_path}")
