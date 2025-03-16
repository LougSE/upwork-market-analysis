import pandas as pd
import numpy as np
from pathlib import Path
import os
from typing import Dict, List, Tuple

def load_prepared_data(data_dir: str) -> pd.DataFrame:
    """Load the prepared data from CSV file."""
    data_file = Path(data_dir) / 'extracted_jobs.csv'
    if not data_file.exists():
        raise FileNotFoundError(f"Data file not found: {data_file}")
    
    return pd.read_csv(data_file)

def get_skill_statistics(df: pd.DataFrame, skill_columns: List[str]) -> Tuple[Dict, pd.Series]:
    """
    Calculate statistics about the encoded skills.
    
    Returns:
        Tuple containing:
        - Dictionary with general statistics
        - Series with skill co-occurrence counts
    """
    stats = {
        'total_jobs': len(df),
        'jobs_with_skills': df[skill_columns].any(axis=1).sum(),
        'avg_skills_per_job': df[skill_columns].sum(axis=1).mean(),
        'max_skills_per_job': df[skill_columns].sum(axis=1).max(),
    }
    
    # Calculate skill co-occurrences
    skill_correlations = df[skill_columns].corr()
    # Get the sum of correlations for each skill (indicates how often it appears with other skills)
    co_occurrences = skill_correlations.sum()
    
    return stats, co_occurrences

def one_hot_encode_skills(df: pd.DataFrame, min_occurrences: int = 5) -> pd.DataFrame:
    """
    Perform one-hot encoding on the skills column efficiently.
    Only include skills that appear at least min_occurrences times.
    
    Args:
        df: DataFrame containing a 'skills' column
        min_occurrences: Minimum number of times a skill must appear to be included
    
    Returns:
        DataFrame with additional columns for each common skill
    """
    # Convert string representation of list to actual list
    df['skills'] = df['skills'].fillna('[]').apply(eval)
    
    # Create a list of all skills
    all_skills = []
    for skills_list in df['skills']:
        if isinstance(skills_list, list):
            all_skills.extend(skills_list)
    
    # Count skill occurrences and filter common skills
    skill_counts = pd.Series(all_skills).value_counts()
    common_skills = skill_counts[skill_counts >= min_occurrences].index
    
    # Create a dictionary to store skill columns
    skill_cols = {}
    for skill in common_skills:
        col_name = f'skill_{skill.lower().replace(" ", "_")}'
        skill_cols[col_name] = df['skills'].apply(
            lambda x: 1 if isinstance(x, list) and skill in x else 0
        )
    
    # Combine original DataFrame with skill columns efficiently
    skill_df = pd.DataFrame(skill_cols)
    return pd.concat([df, skill_df], axis=1)

def print_skill_insights(stats: Dict, co_occurrences: pd.Series, skill_counts: pd.Series) -> None:
    """Print insights about the encoded skills."""
    print("\n=== Skill Analysis Summary ===")
    print(f"\nGeneral Statistics:")
    print(f"- Total jobs analyzed: {stats['total_jobs']}")
    print(f"- Jobs with at least one skill: {stats['jobs_with_skills']} ({stats['jobs_with_skills']/stats['total_jobs']*100:.1f}%)")
    print(f"- Average skills per job: {stats['avg_skills_per_job']:.1f}")
    print(f"- Maximum skills per job: {stats['max_skills_per_job']:.0f}")
    
    print("\nTop 20 Most Common Skills:")
    for skill, count in skill_counts.head(20).items():
        skill_name = skill.replace('skill_', '').replace('_', ' ')
        print(f"- {skill_name}: {int(count)} jobs ({count/stats['total_jobs']*100:.1f}%)")
    
    print("\nTop 10 Most Versatile Skills (frequently appear with other skills):")
    for skill, score in co_occurrences.nlargest(10).items():
        skill_name = skill.replace('skill_', '').replace('_', ' ')
        print(f"- {skill_name}: appears with {score:.1f} other skills on average")

def main():
    # Set up paths using environment variable
    base_path = os.environ.get('DataScienceProjectsPath')
    if not base_path:
        raise EnvironmentError("DataScienceProjectsPath environment variable not set")
    
    project_path = Path(base_path) / '20240517 UPWORK RSS Feed'
    prepared_data_path = project_path / '2-Prepared Data'
    output_path = project_path / '3-Uploaded Data'
    
    # Create output directory if it doesn't exist
    output_path.mkdir(exist_ok=True)
    
    try:
        # Load and process data
        print("Loading data...")
        df = load_prepared_data(str(prepared_data_path))
        
        # Perform one-hot encoding
        print("\nPerforming one-hot encoding of skills...")
        df_encoded = one_hot_encode_skills(df)
        
        # Get skill columns and calculate statistics
        skill_columns = [col for col in df_encoded.columns if col.startswith('skill_')]
        skill_counts = df_encoded[skill_columns].sum()
        stats, co_occurrences = get_skill_statistics(df_encoded, skill_columns)
        
        # Print insights
        print_skill_insights(stats, co_occurrences, skill_counts)
        
        # Save processed data
        output_file = output_path / f'processed_data_{pd.Timestamp.now().strftime("%Y%m%d")}.csv'
        df_encoded.to_csv(output_file, index=False)
        print(f"\nProcessed data saved to: {output_file}")
            
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise

if __name__ == "__main__":
    main()
