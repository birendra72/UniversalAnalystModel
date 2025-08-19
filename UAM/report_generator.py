import os
import markdown
import pdfkit
from typing import Optional
import base64
from datetime import datetime

# Add this function to generate a styled PDF
def generate_styled_pdf(md_content, pdf_path, dataset_name, eda_image_dir=None):
    # Base64 encoded logo
    logo_base64 = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsTAAALEwEAmpwYAAABj0lEQVRYw+2Vz0oCURTFjzMqOiiKqCAW4kd0H4Ef0F1k4LJdCxcVlIugjYgQfYV0Ef1YtGvRqqBFC0FwYVkRgYhFkD+Q0fF6YcJ5vmdGc9GDDJw/3HvPPffMvTMD4D8qB8xZcB0YA1qAEqBqA6jYvVzMk7XgMvAIrALbwDdQBrK2vQc8AVvAOnALvCwLwK4Fdw0oAilgD9gH8sC7cQvGdw0o2P3cMgB2LHgA5A0oA1n7d4CC8Z3m+4u0cG1JgD3gFqgDz0AFuABKwIudV8z3bP6q+fLmWxogb8E3wLkBfQNnwKntL8z3bP6q+fLmWxpgw4JvgJwBfQEnwIntL8z3bP6q+fLmWxpgzYJvgKwBfQJHwLHtL8z3bP6q+fLmWxpg1YJvgLQBfQAHwKHtL8z3bP6q+fLmWxpgxYJvgLQBfQB7wIHtL8z3bP6q+fLmWxpgxYJvgLQBfQBZYN/2F+Z7Nn/VfHnzLQ2wYsE3QNqAPoEMkLP9hfmezV81X958SwOsWPANkDagTyANZG1/Yb5n81fNlzff0gD/L/gL/gH4A3pO9kP0cRwTAAAAAElFTkSuQmCC"

    # Enhanced CSS styling
    css_style = """
    <style>
        @page {
            margin: 1.5cm;
            size: A4;
            @top-center {
                content: "Universal Analyst Report";
                font-family: 'Segoe UI', Tahoma, sans-serif;
                font-size: 10pt;
                color: #2c3e50;
            }
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-family: 'Segoe UI', Tahoma, sans-serif;
                font-size: 9pt;
                color: #7f8c8d;
            }
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #34495e;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            font-size: 11pt;
        }
        img {
             width: 395px;
             height: 300px;
        } 
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #3498db;
        }
        
        .logo {
            width: 70px;
            height: 70px;
        }
        
        .title-section {
            text-align: center;
            flex-grow: 1;
        }
        
        .report-title {
            color: #2c3e50;
            font-size: 22px;
            margin-bottom: 5px;
            font-weight: 600;
        }
        
        .metadata {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 20px;
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            font-size: 10pt;
        }
        
        .metadata-item {
            display: flex;
        }
        
        .metadata-label {
            font-weight: 600;
            min-width: 140px;
            color: #2c3e50;
        }
        
        .metadata-value {
            color: #7f8c8d;
        }
        
        .section {
            margin-bottom: 30px;
            page-break-inside: avoid;
        }
        
        .section-title {
            background-color: #3498db;
            color: white;
            padding: 8px 15px;
            border-radius: 4px;
            font-size: 16px;
            margin-bottom: 15px;
            font-weight: 600;
        }
        
        .subsection {
            margin-bottom: 20px;
            page-break-inside: avoid;
        }
        
        .subsection-title {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
            font-size: 14px;
            margin-bottom: 15px;
            font-weight: 600;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            page-break-inside: avoid;
            font-size: 10pt;
        }
        
        th {
            background-color: #3498db;
            color: white;
            padding: 8px 10px;
            text-align: left;
            font-weight: 600;
        }
        
        td {
            padding: 8px 10px;
            border-bottom: 1px solid #ecf0f1;
        }
        
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        .key-metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .metric-card {
            background: white;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
            padding: 15px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        .metric-value {
            font-size: 20px;
            font-weight: bold;
            color: #3498db;
            margin-bottom: 5px;
        }
        
        .metric-label {
            font-size: 13px;
            color: #7f8c8d;
        }
        
        .visual-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .visual-container {
            text-align: center;
            page-break-inside: avoid;
        }
        
        .visual-title {
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #2c3e50;
        }
        
        .visual-image {
            max-width: 100%;
            max-height: 250px;
            object-fit: contain;
            border: 1px solid #ecf0f1;
            border-radius: 4px;
            padding: 5px;
            background: white;
        }
        
        .insights {
            background-color: #e3f2fd;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin: 20px 0;
            border-radius: 0 4px 4px 0;
            font-size: 11pt;
        }
        
        .insight-item {
            margin-bottom: 8px;
            display: flex;
        }
        
        .insight-item:before {
            content: "•";
            color: #3498db;
            font-weight: bold;
            display: inline-block;
            width: 1em;
            margin-left: -1em;
        }
        
        .model-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }
        
        .model-card {
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 15px;
            background: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        .model-name {
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 10px;
            border-bottom: 1px solid #3498db;
            padding-bottom: 5px;
        }
        
        .footer {
            text-align: center;
            color: #7f8c8d;
            font-size: 10pt;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
        }
        
        /* Better handling for markdown elements */
        h1 { font-size: 20pt; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 8px; }
        h2 { font-size: 16pt; color: #2c3e50; }
        h3 { font-size: 14pt; color: #2c3e50; }
        code { background: #f5f5f5; padding: 2px 5px; border-radius: 3px; }
        pre { background: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto; }
    </style>
    """

    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    
    # Add header with logo and title
    header = f"""
    <div class="header">
        <img class="logo" src="data:image/png;base64,{logo_base64}" alt="Logo">
        <div class="title-section">
            <div class="report-title">Universal Analyst Report</div>
            <div>Comprehensive Analysis of {dataset_name} Dataset</div>
        </div>
    </div>
    
    <div class="metadata">
        <div class="metadata-item">
            <span class="metadata-label">Report Date:</span>
            <span class="metadata-value">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Dataset Name:</span>
            <span class="metadata-value">{dataset_name}</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Analysis Type:</span>
            <span class="metadata-value">Full EDA & Modeling</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Report Version:</span>
            <span class="metadata-value">1.0</span>
        </div>
    </div>
    """
    
    # Create full HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Analysis Report: {dataset_name}</title>
        {css_style}
    </head>
    <body>
        {header}
        {html_content}
        <div class="footer">
            Report generated by Universal Analyst Model | Confidential & Proprietary
        </div>
    </body>
    </html>
    """
    
    # Save HTML to a temp file
    html_path = os.path.join(os.path.dirname(pdf_path), f"{dataset_name}_styled_report.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    # PDF generation options
    options = {
        'page-size': 'A4',
        'margin-top': '1cm',
        'margin-bottom': '1cm',
        'margin-left': '1cm',
        'margin-right': '1cm',
        'encoding': "UTF-8",
        'enable-local-file-access': None,
        'dpi': 300,
        'image-dpi': 300,
        'image-quality': 100,
        'no-outline': None,
        'quiet': ''
    }
    
    # Generate PDF
    pdfkit.from_file(html_path, pdf_path, options=options)
    print(f"Professional PDF report generated at: {pdf_path}")

def generate_full_report(dataset_name: str,
                         step1_metadata: dict,
                         eda_summary_path: str,
                         insight_report_path: str,
                         model_report_path: Optional[str] = None,
                         output_dir: str = "reports",
                         output_formats: list = ["md", "pdf"]):
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_md_path = os.path.join(output_dir, f"{dataset_name}_full_report.md")
    report_pdf_path = os.path.join(output_dir, f"{dataset_name}_full_report.pdf")

    # Read EDA summary markdown content
    eda_summary_content = ""
    if os.path.exists(eda_summary_path):
        with open(eda_summary_path, 'r', encoding='utf-8') as f:
            eda_summary_content = f.read()

    # Read Insight report markdown content
    insight_content = ""
    if os.path.exists(insight_report_path):
        with open(insight_report_path, 'r', encoding='utf-8') as f:
            insight_content = f.read()

    # Read Model report markdown content if available
    model_content = ""
    if model_report_path and os.path.exists(model_report_path):
        with open(model_report_path, 'r', encoding='utf-8') as f:
            model_content = f.read()

    # Compose full markdown report
    with open(report_md_path, 'w', encoding='utf-8') as f:
        f.write(f"# Universal Analyst Model Report\n\n")
        f.write(f"**Date of Analysis:** {date_str}\n\n")
        f.write(f"**Dataset:** {dataset_name}\n\n")
        f.write("## Step 1: Dataset Overview\n")
        for key, value in step1_metadata.items():
            f.write(f"- {key}: {value}\n")
        f.write("\n")
        f.write("## Step 2: Exploratory Data Analysis (EDA)\n")
        f.write(eda_summary_content + "\n")
        f.write("## Step 3: Insight Extraction\n")
        f.write(insight_content + "\n")
        if model_content:
            f.write("## Step 4: Modeling and Prediction\n")
            f.write(model_content + "\n")
        f.write("## Conclusion\n")
        f.write("This report summarizes the data ingestion, preprocessing, exploratory analysis, insights, and modeling results.\n")
        f.write("Further analysis and model tuning may be required based on business needs.\n")
    # Convert to PDF if requested
    if "pdf" in output_formats:
        try:
            # Read the markdown report
            with open(report_md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Generate styled PDF
            generate_styled_pdf(
                md_content, 
                report_pdf_path, 
                dataset_name,
                eda_image_dir="eda_outputs/"  # Path to your visualization images
            )
            print(f"Professional PDF report generated at: {report_pdf_path}")
        except Exception as e:
            print(f"Failed to generate PDF report: {e}")

    print(f"Markdown report generated at: {report_md_path}")
