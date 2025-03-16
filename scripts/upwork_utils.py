import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd

def extract_tag_content(text: str, tag: str) -> Optional[str]:
    """Extract content between <b>tag</b>: and the next HTML tag or newline."""
    pattern = f'<b>{tag}</b>:\s*([^<\n]+)'
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None

def parse_hourly_range(range_str: str) -> Dict[str, float]:
    """Parse hourly range string into min and max values."""
    if not range_str:
        return {'min_rate': None, 'max_rate': None}
    
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
    
    match = re.search(r'\$?(\d+(?:\.\d+)?)', budget_str)
    return float(match.group(1)) if match else None

def parse_skills(skills_str: str) -> List[str]:
    """Parse skills string into list of individual skills."""
    if not skills_str:
        return []
    
    skills = [skill.strip() for skill in skills_str.split(',')]
    return [skill for skill in skills if skill]

def parse_posted_date(date_str: str) -> Optional[str]:
    """Parse posted date string into ISO format."""
    if not date_str:
        return None
    
    try:
        dt = datetime.strptime(date_str.strip(), "%B %d, %Y %H:%M UTC")
        return dt.isoformat()
    except ValueError:
        return None

def extract_technical_context(description: str) -> Dict[str, List[str]]:
    """Extract technical context from job description."""
    context = {
        'data_sources': [],
        'integrations': [],
        'technologies': [],
        'infrastructure': []
    }
    
    # Common data sources
    data_sources = ['SQL Server', 'PostgreSQL', 'MySQL', 'Oracle', 'Snowflake', 'MongoDB', 'Excel']
    integrations = ['AirByte', 'Fivetran', 'Zapier', 'Azure Data Factory', 'SSIS', 'NetSuite']
    technologies = ['DAX', 'Power Query', 'M Language', 'Python', 'R', 'SQL']
    infrastructure = ['AWS', 'Azure', 'GCP', 'On-premise']
    
    for source in data_sources:
        if re.search(rf'\b{source}\b', description, re.IGNORECASE):
            context['data_sources'].append(source)
    
    for integration in integrations:
        if re.search(rf'\b{integration}\b', description, re.IGNORECASE):
            context['integrations'].append(integration)
    
    for tech in technologies:
        if re.search(rf'\b{tech}\b', description, re.IGNORECASE):
            context['technologies'].append(tech)
    
    for infra in infrastructure:
        if re.search(rf'\b{infra}\b', description, re.IGNORECASE):
            context['infrastructure'].append(infra)
    
    return context

def extract_project_requirements(description: str) -> Dict[str, any]:
    """Extract project requirements and characteristics."""
    requirements = {
        'duration_type': None,  # 'one-time' or 'ongoing'
        'expertise_level': None,  # 'beginner', 'intermediate', 'expert'
        'team_size': None,  # 'individual' or 'team'
        'certifications_required': False
    }
    
    # Duration type
    if re.search(r'\b(one[ -]time|single|one off)\b', description, re.IGNORECASE):
        requirements['duration_type'] = 'one-time'
    elif re.search(r'\b(ongoing|long[ -]term|continuous)\b', description, re.IGNORECASE):
        requirements['duration_type'] = 'ongoing'
    
    # Expertise level
    if re.search(r'\b(expert|senior|advanced|experienced)\b', description, re.IGNORECASE):
        requirements['expertise_level'] = 'expert'
    elif re.search(r'\b(intermediate|mid[ -]level)\b', description, re.IGNORECASE):
        requirements['expertise_level'] = 'intermediate'
    elif re.search(r'\b(junior|entry[ -]level|beginner)\b', description, re.IGNORECASE):
        requirements['expertise_level'] = 'beginner'
    
    # Team size
    if re.search(r'\b(team|collaborate|work with|multiple|other|developers)\b', description, re.IGNORECASE):
        requirements['team_size'] = 'team'
    else:
        requirements['team_size'] = 'individual'
    
    # Certifications
    if re.search(r'\b(certifi|qualification|certified)\b', description, re.IGNORECASE):
        requirements['certifications_required'] = True
    
    return requirements

def extract_job_data(item: Dict) -> Dict:
    """Extract all relevant data from a job listing."""
    description = item.get('description', '')
    
    # Extract basic info
    country = extract_tag_content(description, 'Country')
    category = extract_tag_content(description, 'Category')
    skills_str = extract_tag_content(description, 'Skills')
    posted_on = extract_tag_content(description, 'Posted On')
    hourly_range = extract_tag_content(description, 'Hourly Range')
    budget = extract_tag_content(description, 'Budget')
    
    # Parse complex fields
    rate_info = parse_hourly_range(hourly_range)
    
    # Extract additional context
    tech_context = extract_technical_context(description)
    project_reqs = extract_project_requirements(description)
    
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
        'raw_description': description,
        # Additional extracted information
        'data_sources': tech_context['data_sources'],
        'integrations': tech_context['integrations'],
        'technologies': tech_context['technologies'],
        'infrastructure': tech_context['infrastructure'],
        'duration_type': project_reqs['duration_type'],
        'expertise_level': project_reqs['expertise_level'],
        'team_size': project_reqs['team_size'],
        'certifications_required': project_reqs['certifications_required']
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
