# 🌐 Universal Analyst Model (UAM)

A comprehensive data analytics and machine learning platform that provides automated data analysis, visualization, and predictive modeling capabilities through both web and programmatic interfaces.

## 🚀 Working Features

### ✅ Core Functionality (Currently Active)

#### 1. **Multi-format Data Loading**
- **CSV files** - Full support with automatic delimiter detection
- **Excel files** - Both .xlsx and .xls formats with sheet selection
- **JSON files** - Nested JSON support with flattening capabilities
- **SQL Databases** - SQLite, MySQL, PostgreSQL connectivity
- **Data Validation** - Automatic schema detection and type inference

#### 2. **Automated Data Preprocessing**
- **Missing Value Handling** - Median/mode imputation with configurable thresholds
- **Feature Selection** - Removes constant and highly correlated features (configurable correlation threshold)
- **Data Type Detection** - Automatic numerical, categorical, datetime detection
- **Outlier Detection** - Statistical outlier identification and handling
- **PCA Integration** - Automatic dimensionality reduction for high-dimensional datasets

#### 3. **Interactive Web Interface (Streamlit)**
- **Home Dashboard** - Project overview and quick start guide
- **Data Upload** - Drag-and-drop file upload with preview
- **Exploratory Data Analysis (EDA)** - Automated statistical summaries and visualizations
- **Insights Generation** - Automated pattern discovery and key findings
- **Natural Language Query** - Plain English queries converted to SQL
- **Modeling Interface** - Point-and-click machine learning model training
- **Report Generation** - Automated PDF/HTML reports with visualizations

#### 4. **Comprehensive EDA Engine**
- **Statistical Summaries** - Mean, median, mode, standard deviation, quartiles
- **Distribution Analysis** - Histograms, box plots, violin plots
- **Correlation Analysis** - Heatmaps, scatter plots, correlation matrices
- **Categorical Analysis** - Bar charts, pie charts, count plots
- **Missing Value Visualization** - Missingno matrices and bar charts

#### 5. **Machine Learning Pipeline**
- **AutoML Classification** - Logistic Regression, Random Forest, SVM
- **AutoML Regression** - Linear Regression, Random Forest Regressor
- **Model Evaluation** - Cross-validation, confusion matrices, classification reports
- **Feature Importance** - Built-in feature importance ranking
- **Model Persistence** - Save/load trained models for deployment

#### 6. **Natural Language Query Interface**
- **Plain English to SQL** - Convert natural language questions to SQL queries
- **Real-time Results** - Execute queries on in-memory datasets
- **Query History** - Track and reuse previous queries
- **Export Results** - Download query results as CSV/Excel

#### 7. **Automated Report Generation**
- **PDF Reports** - Professional reports with visualizations and insights
- **HTML Reports** - Interactive web-based reports
- **Markdown Reports** - GitHub-compatible documentation
- **Customizable Templates** - Configurable report sections and styling

### 📊 Visualization Capabilities
- **Interactive Charts** - Zoom, pan, hover tooltips
- **Multiple Chart Types** - Bar, line, scatter, heatmap, box plots
- **Color Themes** - Professional color schemes
- **Export Options** - PNG, SVG, PDF formats
- **Responsive Design** - Mobile-friendly visualizations

### 🛠️ Technical Architecture

#### **Backend Components**
- **Data Loader** (`UAM/data_loader.py`) - Multi-source data ingestion
- **EDA Engine** (`UAM/eda_engine.py`) - Automated exploratory analysis
- **Insight Extractor** (`UAM/insight_extractor.py`) - Pattern discovery
- **Modeling** (`UAM/modeling.py`) - ML model training and evaluation
- **NL Query Interface** (`UAM/nl_query_interface.py`) - Natural language processing
- **Report Generator** (`UAM/report_generator.py`) - Automated reporting

#### **Frontend Components**
- **Streamlit App** (`main_app.py`) - Main web interface
- **Data Upload** (`data_upload_app.py`) - File upload interface
- **EDA Module** (`eda_app.py`) - Interactive EDA dashboard
- **NL Query** (`nl_query.py`) - Natural language query interface
- **Modeling** (`modeling_app.py`) - ML model training interface
- **Report** (`report_app.py`) - Report generation interface

### 🎯 Supported Data Types
- **Numerical** - Integers, floats, continuous/discrete variables
- **Categorical** - Nominal and ordinal categories
- **Datetime** - Date and time series data
- **Text** - String and text-based features
- **Boolean** - True/false binary data

### 📈 Model Performance Metrics
- **Classification** - Accuracy, precision, recall, F1-score, ROC-AUC
- **Regression** - R², RMSE, MAE, MAPE
- **Cross-validation** - K-fold validation with configurable folds
- **Feature Importance** - Permutation importance and SHAP values

## 🚀 Quick Start

### Web Interface (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Launch Streamlit app
streamlit run main_app.py
```

### Programmatic Usage
```python
from UAM import data_loader, eda_engine, modeling

# Load data
df = data_loader.load_data('csv', {'filepath': 'data.csv'})

# Preprocess
processed_df, metadata, _ = data_loader.preprocess_data(df)

# Generate insights
insights = insight_extractor.run_insight_extraction(processed_df)

# Train model
model, metrics = modeling.train_model(processed_df, target_column='target')
```

## 📋 Requirements

### Core Dependencies
- **Python 3.7+**
- **Streamlit** - Web interface framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning
- **Matplotlib/Seaborn** - Visualization
- **OpenAI API** - Natural language processing

### Optional Dependencies
- **SQLAlchemy** - Database connectivity
- **DuckDB** - In-memory SQL processing
- **WeasyPrint** - PDF report generation

## 🎯 Use Cases

### Business Analytics
- Customer segmentation and profiling
- Sales forecasting and trend analysis
- Marketing campaign effectiveness
- Financial risk assessment

### Research & Academia
- Scientific data analysis
- Survey data processing
- Experimental result visualization
- Thesis data exploration

### Operations
- Quality control monitoring
- Supply chain optimization
- Resource allocation analysis
- Performance tracking

## 🔧 Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your_openai_key_here
```

### Custom Settings
- **Correlation threshold** - Configurable feature correlation limit
- **Missing value threshold** - Data quality threshold
- **PCA variance** - Dimensionality reduction parameter
- **Cross-validation folds** - Model validation settings

## 📊 Example Outputs

### Sample Reports
- **EDA Report** - Statistical summaries and visualizations
- **Model Report** - Training results and performance metrics
- **Insights Report** - Key findings and recommendations

### Sample Visualizations
- **Correlation Heatmap** - Feature relationships
- **Distribution Plots** - Data distribution analysis
- **Feature Importance** - Model interpretability
- **Prediction Results** - Model performance visualization

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for details on how to submit pull requests, report issues, or suggest new features.

## 🆘 Support

For support, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ by the UAM Development Team**
