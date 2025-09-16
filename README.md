# Citizen Complaint Analysis Tool

A simple web application for analyzing citizen complaint data from Excel files. This tool processes complaint data and generates comprehensive reports showing complaint patterns by subcategory, individuals, and households across different atolls and islands.

## Features

- **File Upload Interface**: Clean, modern web interface for uploading Excel files
- **Comprehensive Analysis**: Three types of analysis for each location (atoll/island):
  1. Complaint count analysis (total complaints by subcategory)
  2. Individual analysis (unique individuals reporting complaints)
  3. Household analysis (unique households reporting complaints)
- **Geographic Breakdown**: Separate analysis for each atoll and island
- **Top 20 Results**: Shows the top 20 results for each analysis type
- **Percentage Calculations**: Includes percentages of total complaints, surveyed individuals/households, and total population
- **HTML Report Generation**: Downloads formatted HTML reports

## Required Data Format

Your Excel file should contain the following columns:

- `category` - Complaint category (Dhivehi or English)
- `subcategory` - Complaint subcategory (Dhivehi or English)  
- `person_id` - Unique identifier for each person
- `household_id` - Unique identifier for each household
- `row_id` - Unique identifier for each complaint record
- `island` - Island name where complaint was made
- `atoll` - Atoll name where complaint was made

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the Web Interface**:
   Open your browser and go to `http://localhost:5000`

## Usage

1. **Upload Excel File**: Use the web interface to upload your complaint data Excel file
2. **Automatic Processing**: The tool will automatically process your data and perform all analyses
3. **Download Report**: A comprehensive HTML report will be automatically downloaded containing:
   - Summary statistics
   - Analysis by atoll (top 20 for each analysis type)
   - Analysis by island (top 20 for each analysis type)
   - Detailed tables with counts and percentages

## Analysis Types

### 1. Complaint Count Analysis
- Shows subcategories ranked by total number of complaints
- Includes percentage of total complaints for each subcategory

### 2. Individual Analysis  
- Shows subcategories ranked by number of unique individuals reporting complaints
- Includes percentage of surveyed individuals who made each complaint
- Includes percentage of total population who made each complaint (when population data available)

### 3. Household Analysis
- Shows subcategories ranked by number of unique households reporting complaints  
- Includes percentage of surveyed households who made each complaint
- Includes percentage of total households who made each complaint (when population data available)

## File Structure

```
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Web interface template
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── uploads/             # Temporary upload directory (created automatically)
```

## Technical Details

- **Framework**: Flask (Python web framework)
- **Data Processing**: Pandas for Excel file handling and data analysis
- **UI**: Bootstrap 5 for modern, responsive design
- **Output**: HTML reports with formatted tables
- **File Support**: Excel files (.xlsx, .xls)

## Notes

- The application automatically creates necessary directories
- Uploaded files are processed and then cleaned up automatically
- Reports are generated as HTML files for easy viewing and sharing
- The tool handles both Dhivehi and English labels (translation support can be added)
- Population data integration is supported for enhanced percentage calculations

## Support

For issues or questions, please check that your Excel file contains all required columns and follows the specified format.
