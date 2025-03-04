# Original Data

This folder contains the raw, unmodified data collected from Upwork RSS feeds. This data serves as our source of truth and should never be modified.

## Contents
- RSS feed XML files (YYYYMMDD_RSS_PowerBI.xml)
- Converted JSON files (YYYYMMDD_RSS_PowerBI.json)

## Purpose
- Preserve original data in its raw form
- Enable data recovery if needed
- Maintain data lineage and audit trail

## Data Collection
- Automated collection every 2 days via scheduled scripts
- Files are named with date stamps for easy tracking
- Both XML and JSON formats are preserved

## Usage Guidelines
- ⚠️ NEVER modify files in this folder
- Always work with copies in the Prepared Data folder
- Maintain file naming convention: YYYYMMDD_RSS_PowerBI.[xml|json]