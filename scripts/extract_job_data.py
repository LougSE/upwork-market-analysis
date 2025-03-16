import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd

#Load environement variables
pathenv = "DataScienceProjectsPath"
subpath = os.getenv(pathenv)
dubpath = r"20240517 UPWORK RSS Feed\2-Prepared Data\RawFiles"

# Directory to save the file
files_directory = os.path.join(subpath,dubpath)

def extract_tag_content(text: str, tag: str) -> Optional[str]:
    """Extract content between <b>tag</b>: and the next HTML tag or newline."""
    pattern = f'<b>{tag}</b>:\s*([^<\n]+)'
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None

def parse_hourly_range(range_str: str) -> Dict[str, float]:
    """Parse hourly range string into min and max values."""
    if not range_str:
        return {'min_rate': None, 'max_rate': None}
    
    # Extract numbers from string like "$20.00-$45.00"
    numbers = re.findall(r'\$?(\d+(?:\.\d+)?)', range_str)
    if len(numbers) >= 2:
        return {
            'min_rate': float(numbers[0]),
            'max_rate': float(numbers[1])
        }
    elif len(numbers) == 1:
        return {
            'min_rate': float(numbers[0]),
            'max_rate': float(numbers[0])
        }
    return {'min_rate': None, 'max_rate': None}

def parse_budget(budget_str: str) -> float:
    """Parse fixed budget string into a number."""
    if not budget_str:
        return None
    
    # Extract number from string like "$500"
    match = re.search(r'\$?(\d+(?:\.\d+)?)', budget_str)
    return float(match.group(1)) if match else None

def parse_skills(skills_str: str) -> List[str]:
    """Parse skills string into list of individual skills."""
    if not skills_str:
        return []
    
    # Split by comma and clean each skill
    skills = [skill.strip() for skill in skills_str.split(',')]
    return [skill for skill in skills if skill]  # Remove empty strings

def parse_posted_date(date_str: str) -> Optional[str]:
    """Parse posted date string into ISO format."""
    if not date_str:
        return None
    
    try:
        # Parse date string like "August 07, 2024 06:40 UTC"
        dt = datetime.strptime(date_str.strip(), "%B %d, %Y %H:%M UTC")
        return dt.isoformat()
    except ValueError:
        return None

def extract_job_data(item: Dict) -> Dict:
    """Extract all relevant data from a job listing."""
    description = item.get('description', '')
    
    # Extract all tags
    country = extract_tag_content(description, 'Country')
    category = extract_tag_content(description, 'Category')
    skills_str = extract_tag_content(description, 'Skills')
    posted_on = extract_tag_content(description, 'Posted On')
    hourly_range = extract_tag_content(description, 'Hourly Range')
    budget = extract_tag_content(description, 'Budget')
    
    # Parse the complex fields
    rate_info = parse_hourly_range(hourly_range)
    
    return {
        'title': item.get('title', ''),
        'link': item.get('link', ''),
        'country': country,
        'category': category,
        'skills': parse_skills(skills_str),
        'posted_date': parse_posted_date(posted_on),
        'is_hourly': bool(hourly_range),
        'min_rate': rate_info['min_rate'],
        'max_rate': rate_info['max_rate'],
        'fixed_budget': parse_budget(budget),
        'raw_description': description
    }

def process_json_files(directory: str) -> pd.DataFrame:
    """Process all JSON files in directory and return a DataFrame."""
    all_jobs = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    items = data['rss']['channel']['item']
                    
                    # Process each job listing
                    for item in items:
                        job_data = extract_job_data(item)
                        job_data['source_file'] = filename
                        all_jobs.append(job_data)
                        
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    # Convert to DataFrame
    df = pd.DataFrame(all_jobs)
    
    # Add collection date from filename
    df['collection_date'] = pd.to_datetime(df['source_file'].str.extract(r'(\d{8})')[0], format='%Y%m%d')
    
    return df

if __name__ == "__main__":
    # Directory containing the JSON files
    json_dir = files_directory
    
    # Process all files
    df = process_json_files(json_dir)
    
    # Save to CSV in the Prepared Data directory
    output_dir = os.path.dirname(os.path.dirname(json_dir))
    output_file = os.path.join(output_dir, 'extracted_jobs.csv')
    df.to_csv(output_file, index=False)
    
    # Print summary
    print("\nData Extraction Summary:")
    print("-" * 50)
    print(f"Total jobs processed: {len(df)}")
    print(f"\nSample of extracted data:")
    print(df[['title', 'country', 'category', 'min_rate', 'max_rate', 'fixed_budget']].head())
    print(f"\nOutput saved to: {output_file}")
