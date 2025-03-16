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
