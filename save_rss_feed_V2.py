import requests
import os
from datetime import datetime
import xmltodict
import json

#Load environement variables
pathenv = "DataScienceProjectsPath"
subpath = os.getenv(pathenv)
dubpath = r"20240517 UPWORK RSS Feed\1-Original Data"


# Directory to save the files
save_directory = os.path.join(subpath,dubpath)


# RSS feed URL
rss_url = "https://www.upwork.com/ab/feed/jobs/rss?paging=0-10&q=Power%20Bi&sort=recency&api_params=1&securityToken=d17308910f66b74d222ca66c907efa56c942739d41db7bba3da3ca225a9584b2edcab156ed12fcd81a0f94e952ea29d611248991196927c716632e2284293c57&userUid=1729067928257851392&orgUid=1729067928257851393"


#save_directory = r"C:\Users\saadl\OneDrive\Bureau\RSS Files"
os.makedirs(save_directory, exist_ok=True)

# Current date in YYYYMMDD format
current_date = datetime.now().strftime("%Y%m%d")

# Keyword for the file name
keyword = "PowerBI"

# Generate dynamic file names
xml_file_name = f"{current_date}_RSS_{keyword}.xml"
json_file_name = f"{current_date}_RSS_{keyword}.json"
xml_file_path = os.path.join(save_directory, xml_file_name)
json_file_path = os.path.join(save_directory, json_file_name)

# Fetch the RSS feed
response = requests.get(rss_url)

# Check if the request was successful
if response.status_code == 200:
    # Save the RSS feed to a file
    with open(xml_file_path, 'wb') as file:
        file.write(response.content)
    print(f"RSS feed saved successfully as {xml_file_name}.")
    
    # Convert XML to JSON
    with open(xml_file_path, 'r') as xml_file:
        xml_content = xml_file.read()
        json_data = xmltodict.parse(xml_content)
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
    print(f"Converted JSON saved successfully as {json_file_name}.")
else:
    print("Failed to fetch the RSS feed. Status code:", response.status_code)
