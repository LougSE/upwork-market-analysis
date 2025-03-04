# Scripts Documentation

This folder contains all automation and data collection scripts used in the project.

## Script Overview

### RSS Feed Collection
- `save_rss_feed.py`: Main script for collecting Upwork RSS feed data
- `save_rss_feed_V2.py`: Enhanced version with improved error handling and logging

### Scheduled Tasks
- `upwork_powerbi_rss.bat`: Windows scheduled task for automated data collection
- `upwork_powerbi_rss_V2.bat`: Updated version with additional parameters

### Data Processing
- `XmlToJsonScript.ipynb`: Converts XML feed data to structured JSON format

## Usage

1. **RSS Feed Collection**
   - Runs automatically via Windows Task Scheduler
   - Can be manually triggered if needed
   - Saves data to the `1-Original Data` folder

2. **Scheduled Tasks**
   - Configured in Windows Task Scheduler
   - Runs every 2 days to collect fresh data
   - Logs execution status

3. **Data Processing**
   - Used for converting and structuring collected data
   - Prepares data for PowerBI integration

## Configuration

- Environment variables required:
  - `DataScienceProjectsPath`: Base path for project
  - `OpenAIKeyLougse1`: OpenAI API key (for GPT processing)

## Error Handling

All scripts include:
- Basic error logging
- Retry mechanisms for API calls
- Data validation checks
