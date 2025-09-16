"""
Citizen Complaint Analysis Web Application

This Flask web app allows users to upload Excel files containing citizen complaint data
and generates comprehensive analysis reports showing complaint patterns by subcategory,
individuals, and households across different atolls and islands.

The app processes complaint data with categories, subcategories, person_id, household_id,
row_id, island, and atoll information to provide detailed statistical analysis.
"""

from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
import pandas as pd
import numpy as np
from io import BytesIO
import os
from werkzeug.utils import secure_filename
import tempfile
from datetime import datetime
import base64

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Configuration for file uploads
UPLOAD_FOLDER = '/tmp/uploads'  # Use /tmp for Vercel
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension
    
    Args:
        filename (str): Name of the uploaded file
        
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_complaint_data(file_path, translation_file_path=None, population_file_path=None):
    """
    Process the uploaded Excel file containing complaint data
    
    Args:
        file_path (str): Path to the uploaded complaint data file
        translation_file_path (str): Path to translation file (optional)
        population_file_path (str): Path to population data file (optional)
        
    Returns:
        dict: Dictionary containing processed data and analysis results
    """
    try:
        # Read the main complaint data
        df = pd.read_excel(file_path)
        
        # Validate required columns exist
        required_columns = ['category', 'subcategory', 'person_id', 'household_id', 'row_id', 'island', 'atoll']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Read translation data if provided
        translation_df = None
        if translation_file_path and os.path.exists(translation_file_path):
            translation_df = pd.read_excel(translation_file_path)
        
        # Read population data if provided
        population_df = None
        if population_file_path and os.path.exists(population_file_path):
            population_df = pd.read_excel(population_file_path)
        
        # Apply translations if available
        if translation_df is not None:
            # Merge with translation data to get English labels
            df = df.merge(translation_df, on=['category', 'subcategory'], how='left')
            # Use English labels if available, otherwise keep original
            df['subcategory_en'] = df.get('subcategory_en', df['subcategory'])
            df['category_en'] = df.get('category_en', df['category'])
        else:
            df['subcategory_en'] = df['subcategory']
            df['category_en'] = df['category']
        
        # Perform analysis
        results = perform_analysis(df, population_df)
        
        return {
            'success': True,
            'data': results,
            'total_complaints': len(df),
            'total_individuals': df['person_id'].nunique(),
            'total_households': df['household_id'].nunique()
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def perform_analysis(df, population_df=None):
    """
    Perform comprehensive analysis of complaint data
    
    Args:
        df (DataFrame): Processed complaint data
        population_df (DataFrame): Population data (optional)
        
    Returns:
        dict: Analysis results organized by atoll and island
    """
    results = {}
    
    # Analysis by Atoll
    results['by_atoll'] = analyze_by_location(df, 'atoll', population_df)
    
    # Analysis by Island
    results['by_island'] = analyze_by_location(df, 'island', population_df)
    
    return results

def analyze_by_location(df, location_col, population_df=None):
    """
    Analyze complaints by location (atoll or island)
    
    Args:
        df (DataFrame): Complaint data
        location_col (str): Column name for location ('atoll' or 'island')
        population_df (DataFrame): Population data (optional)
        
    Returns:
        dict: Analysis results for the specified location type
    """
    location_results = {}
    
    # Get unique locations
    locations = df[location_col].unique()
    
    for location in locations:
        location_data = df[df[location_col] == location]
        
        # Analysis 1: Count by subcategory (total complaints)
        subcategory_counts = location_data['subcategory_en'].value_counts()
        subcategory_percentages = (subcategory_counts / len(location_data) * 100).round(2)
        
        # Analysis 2: Count by unique individuals
        individual_counts = location_data.groupby('subcategory_en')['person_id'].nunique().sort_values(ascending=False)
        total_individuals = location_data['person_id'].nunique()
        individual_percentages = (individual_counts / total_individuals * 100).round(2)
        
        # Analysis 3: Count by unique households
        household_counts = location_data.groupby('subcategory_en')['household_id'].nunique().sort_values(ascending=False)
        total_households = location_data['household_id'].nunique()
        household_percentages = (household_counts / total_households * 100).round(2)
        
        # Get population data if available
        population_info = {}
        if population_df is not None:
            pop_data = population_df[population_df[location_col] == location]
            if not pop_data.empty:
                population_info = {
                    'total_population': pop_data.iloc[0].get('total_population', 0),
                    'total_households': pop_data.iloc[0].get('total_households', 0)
                }
        
        # Calculate population percentages if population data is available
        individual_pop_percentages = {}
        household_pop_percentages = {}
        
        if population_info.get('total_population', 0) > 0:
            individual_pop_percentages = (individual_counts / population_info['total_population'] * 100).round(2)
        
        if population_info.get('total_households', 0) > 0:
            household_pop_percentages = (household_counts / population_info['total_households'] * 100).round(2)
        
        location_results[location] = {
            'subcategory_counts': subcategory_counts.head(20),
            'subcategory_percentages': subcategory_percentages.head(20),
            'individual_counts': individual_counts.head(20),
            'individual_percentages': individual_percentages.head(20),
            'individual_pop_percentages': individual_pop_percentages.head(20),
            'household_counts': household_counts.head(20),
            'household_percentages': household_percentages.head(20),
            'household_pop_percentages': household_pop_percentages.head(20),
            'population_info': population_info,
            'summary': {
                'total_complaints': len(location_data),
                'total_individuals': total_individuals,
                'total_households': total_households
            }
        }
    
    return location_results

def generate_report(results):
    """
    Generate a formatted report from analysis results
    
    Args:
        results (dict): Analysis results from perform_analysis
        
    Returns:
        str: HTML formatted report
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Citizen Complaint Analysis Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1, h2, h3 { color: #2c3e50; }
            table { border-collapse: collapse; width: 100%; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #3498db; color: white; }
            .location-section { margin: 30px 0; }
            .analysis-section { margin: 20px 0; }
        </style>
    </head>
    <body>
        <h1>Citizen Complaint Analysis Report</h1>
        <p>Generated on: {}</p>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Add summary statistics
    html_content += "<h2>Summary Statistics</h2>"
    html_content += "<p>Total Complaints: {}</p>".format(results.get('total_complaints', 0))
    html_content += "<p>Total Individuals: {}</p>".format(results.get('total_individuals', 0))
    html_content += "<p>Total Households: {}</p>".format(results.get('total_households', 0))
    
    # Process each location type (atoll and island)
    for location_type, location_data in results['data'].items():
        html_content += f"<div class='location-section'>"
        html_content += f"<h2>Analysis by {location_type.replace('_', ' ').title()}</h2>"
        
        for location, analysis in location_data.items():
            html_content += f"<h3>{location}</h3>"
            
            # Analysis 1: Subcategory counts
            html_content += "<div class='analysis-section'>"
            html_content += "<h4>Top 20 Complaint Subcategories (by total complaints)</h4>"
            html_content += "<table><tr><th>Subcategory</th><th>Count</th><th>Percentage of Total Complaints</th></tr>"
            
            for subcategory, count in analysis['subcategory_counts'].items():
                percentage = analysis['subcategory_percentages'].get(subcategory, 0)
                html_content += f"<tr><td>{subcategory}</td><td>{count}</td><td>{percentage}%</td></tr>"
            
            html_content += "</table></div>"
            
            # Analysis 2: Individual counts
            html_content += "<div class='analysis-section'>"
            html_content += "<h4>Top 20 Complaint Subcategories (by unique individuals)</h4>"
            html_content += "<table><tr><th>Subcategory</th><th>Unique Individuals</th><th>% of Surveyed Individuals</th><th>% of Total Population</th></tr>"
            
            for subcategory, count in analysis['individual_counts'].items():
                individual_pct = analysis['individual_percentages'].get(subcategory, 0)
                pop_pct = analysis['individual_pop_percentages'].get(subcategory, 0)
                html_content += f"<tr><td>{subcategory}</td><td>{count}</td><td>{individual_pct}%</td><td>{pop_pct}%</td></tr>"
            
            html_content += "</table></div>"
            
            # Analysis 3: Household counts
            html_content += "<div class='analysis-section'>"
            html_content += "<h4>Top 20 Complaint Subcategories (by unique households)</h4>"
            html_content += "<table><tr><th>Subcategory</th><th>Unique Households</th><th>% of Surveyed Households</th><th>% of Total Households</th></tr>"
            
            for subcategory, count in analysis['household_counts'].items():
                household_pct = analysis['household_percentages'].get(subcategory, 0)
                pop_pct = analysis['household_pop_percentages'].get(subcategory, 0)
                html_content += f"<tr><td>{subcategory}</td><td>{count}</td><td>{household_pct}%</td><td>{pop_pct}%</td></tr>"
            
            html_content += "</table></div>"
        
        html_content += "</div>"
    
    html_content += "</body></html>"
    return html_content

@app.route('/')
def index():
    """Main page with file upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    if 'file' not in request.files:
        if request.is_json:
            return jsonify({'error': 'No file selected'}), 400
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        if request.is_json:
            return jsonify({'error': 'No file selected'}), 400
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Process the file
        result = process_complaint_data(file_path)
        
        if result['success']:
            # Generate report
            report_html = generate_report(result)
            
            # For Vercel, return the HTML content directly
            if request.is_json:
                # Return as base64 encoded string for API calls
                html_bytes = report_html.encode('utf-8')
                html_base64 = base64.b64encode(html_bytes).decode('utf-8')
                return jsonify({
                    'success': True,
                    'report_html': html_base64,
                    'filename': 'complaint_analysis_report.html'
                })
            else:
                # Return as file download for web form
                return send_file(
                    BytesIO(report_html.encode('utf-8')),
                    as_attachment=True,
                    download_name='complaint_analysis_report.html',
                    mimetype='text/html'
                )
        else:
            if request.is_json:
                return jsonify({'error': f'Error processing file: {result["error"]}'}), 400
            flash(f'Error processing file: {result["error"]}')
            return redirect(url_for('index'))
    
    error_msg = 'Invalid file type. Please upload an Excel file (.xlsx or .xls)'
    if request.is_json:
        return jsonify({'error': error_msg}), 400
    flash(error_msg)
    return redirect(url_for('index'))

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """API endpoint for file upload and processing"""
    return upload_file()

if __name__ == '__main__':
    app.run(debug=True)
