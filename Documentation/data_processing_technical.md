# Data Processing Technical Documentation

## Overview
This document provides technical details about the data processing components of the Upwork PowerBI Market Analysis system.

## Skills Processing (`process_skills.py`)

### Purpose
Transforms raw job listing data into a structured format with one-hot encoded skills for analysis in PowerBI.

### Key Components

#### 1. Data Loading
```python
def load_prepared_data(data_dir: str) -> pd.DataFrame:
```
- Loads data from `extracted_jobs.csv` in the Prepared Data directory
- Validates file existence before loading
- Returns pandas DataFrame with raw job data

#### 2. Skills One-Hot Encoding
```python
def one_hot_encode_skills(df: pd.DataFrame, min_occurrences: int = 5) -> pd.DataFrame:
```
- Converts string representation of skills to binary columns
- Parameters:
  - `df`: Input DataFrame with 'skills' column
  - `min_occurrences`: Minimum times a skill must appear to be included (default: 5)
- Returns DataFrame with additional binary columns for each skill

#### 3. Basic Statistics
```python
def print_skill_insights(stats: Dict, skill_counts: pd.Series) -> None:
```
- Calculates basic statistics about encoded skills
- Generates metrics like:
  - Total jobs analyzed
  - Jobs with skills specified
  - Average skills per job
  - Maximum skills per job
- Displays frequency of each skill in the dataset

### Data Flow
1. Raw data loaded from Prepared Data directory
2. Skills extracted and validated
3. One-hot encoding performed for common skills (appearing ≥ 5 times)
4. Basic statistics calculated
5. Results saved to Uploaded Data directory with date stamp

### Output Format
- CSV file with format: `processed_data_YYYYMMDD.csv`
- Contains original columns plus binary skill columns
- Each skill column prefixed with `skill_`
- Skill names normalized (lowercase, spaces to underscores)

### Usage Example
```python
# Set environment variable for project path
os.environ['DataScienceProjectsPath'] = '/path/to/project'

# Run the processing script
python process_skills.py
```

### Dependencies
- pandas
- numpy
- pathlib
- typing (for type hints)

### Error Handling
- Validates file existence before processing
- Handles missing or malformed skills data
- Provides clear error messages for common issues

## PowerBI Implementation

### Data Model Design
The data model follows a star schema design for optimal performance and usability:

#### 1. Fact Table (Job Postings)
- **Key Transformations:**
  - Created unique job ID for each posting
  - Split `posted_date` into:
    - `posted_date` (Date format)
    - `posted_time` (Time format)
  - Calculated `average_rate` from `min_rate` and `max_rate`
  - Removed one-hot encoded skill columns
  - Added relationship key to Skills dimension table

#### 2. Dimension Table (Skills)
- **Structure:**
  - `skill_id` (unique identifier)
  - `skill_name` (normalized skill name)
  - `job_id` (relationship to fact table)
- **Created through:**
  - Unpivoting one-hot encoded skill columns
  - Filtering to keep only rows where skill = 1
  - Generating unique skill IDs

### Data Transformation Steps in PowerBI

1. **Initial Load**
   ```powerquery
   let
       Source = Csv.Document("processed_data_YYYYMMDD.csv"),
       #"Promoted Headers" = Table.PromoteHeaders(Source)
   in
       #"Promoted Headers"
   ```

2. **DateTime Processing**
   ```powerquery
   #"Split DateTime" = Table.AddColumn(
       Source, 
       "posted_time",
       each Time.From([posted_date])
   )
   ```

3. **Rate Calculations**
   ```powerquery
   #"Add Average Rate" = Table.AddColumn(
       Source,
       "average_rate",
       each ([min_rate] + [max_rate]) / 2
   )
   ```

4. **Skills Unpivoting**
   ```powerquery
   #"Unpivoted Skills" = Table.UnpivotOtherColumns(
       Source,
       {"job_id", "title", "link", "country", ...},
       "skill_name",
       "has_skill"
   )
   ```

### Visual Design

#### Brand Identity Integration
- Created custom visuals using Upwork's brand guidelines:
  - Color palette: Upwork green (#6FDA44), white (#FFFFFF), dark gray (#222)
  - Logo integration in headers and backgrounds
  - Custom pictograms for KPIs and metrics

#### Dashboard Components
1. **Headers & Backgrounds**
   - Custom-designed in Canva.com
   - Incorporates Upwork brand elements
   - Professional, clean aesthetic

2. **Visual Elements**
   - Custom pictograms for key metrics
   - Consistent color scheme throughout
   - Branded data visualization styles

### Best Practices Implemented

1. **Performance Optimization**
   - Star schema for efficient querying
   - Appropriate data type settings
   - Optimized relationship cardinality

2. **User Experience**
   - Consistent branding across pages
   - Intuitive navigation layout
   - Clear visual hierarchy

3. **Maintainability**
   - Documented transformation steps
   - Modular design pattern
   - Clear naming conventions

### Future Enhancements
1. Implement incremental refresh
2. Add custom tooltips
3. Create drill-through reports
4. Add advanced DAX measures

## Best Practices
1. **Data Validation**
   - Check input data quality
   - Validate skill formats before processing
   - Handle edge cases (empty skills, malformed lists)

2. **Performance Optimization**
   - Uses efficient DataFrame operations
   - Implements batch processing
   - Optimizes memory usage during encoding

3. **Maintainability**
   - Clear function documentation
   - Type hints for better code understanding
   - Modular design for easy updates

4. **Output Quality**
   - Consistent naming conventions
   - Standardized date formats
   - Clear column naming for PowerBI integration

---
*Last Updated: March 16, 2025*
