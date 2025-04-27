import glob
import os
import requests
import json
from datetime import datetime

input_path = "./extract_clan_FR"
data_path = "./data"
output_path = "./extract_clan_FR"

clansFR = {}
extract = []
old_removed_clan = []

### Extract from txt src file
input_file_path = f"{input_path}/src.txt"
if os.path.isfile(input_file_path):
    print(f"Opening file {input_file_path}")
    text_file = open(input_file_path, "r")
else :
    print("No text file found")

### Extract most recent *_french_clan_list.json from data_path
if not os.path.exists(data_path):
    print("Folder data not found, dying program")
    exit(code=-1)
most_recent_file = glob.glob(f'{data_path}/*_french_clan_list.json')
most_recent_file.sort()
most_recent_file.reverse()
most_recent_file = most_recent_file[0]
if os.path.isfile(most_recent_file):
    print(f"Opening file {most_recent_file}")
    json_file = open(most_recent_file)
    clansFR = json.load(json_file)
else :
    print("No json file found, ending program") 
    exit(code=-1)

### Extract data from all *_removed_clan.json file in folder output_path
if not os.path.exists(output_path):
    print("Folder data not found, dying program")
    exit(code=-1)
most_recent_file = glob.glob(f'{output_path}/*_removed_clan.json')
for rfile in most_recent_file:
    if os.path.isfile(rfile):
        print(f"Opening file {rfile}")
        json_file = open(rfile)
        for item_old_removed_clan in json.load(json_file):
            old_removed_clan.append(item_old_removed_clan)
    else :
        print(f"An error occured, invalid path to json file {rfile}")
old_removed_clan.sort()

### Extracting data from input file
print("=== Extracting data from file ===")
for lines in text_file:
    items = lines.split()
    for item in items:
        extract.append(item)

print(f"Found {len(extract)} clans in file")

### Removing duplicates in clan tag
print("=== Cleaning data ===")
before_removing_duplicates = len(extract)
extract = list(set(extract))
extract.sort()
print(f"Removed {str(before_removing_duplicates - len(extract))} duplicate elements")

### Removing already known clans
before_removing_duplicates = len(extract)

known_clans = set([e['clan_tag'] for e in clansFR.values()])
print(f"Found {len(known_clans)} already repertoried clans")

extract_clean = []
for clan in extract:
    if clan not in known_clans and clan not in old_removed_clan:
        extract_clean.append(clan)
extract = extract_clean
print(f"Found {len(extract_clean)} new clans in file")

### Collecting data from API
base_url = 'https://api.worldoftanks.eu/wgn/clans/list/?application_id=6267be451d158341277b1a61f3e32e97&fields=clan_id%2Cname%2Ctag&game=wot&language=fr&search='
MAX_RETRY = 3

print("=== Contacting Wargaming API to get clan data like id and full name ===")

removed_clan = []
for clan in extract:
    print(f"Requesting WG API for clan {clan} \t\t\t........ {extract.index(clan)+1}/{str(len(extract))}")
    for _ in range(MAX_RETRY):
        try:
            response = requests.get(base_url+clan)
        except requests.exceptions.ConnectionError:
            print("Connection error")
            pass

    result = response.json()
    if result["meta"]["count"] >= 1:
        clan_api_info = result["data"][0]
        if clan == clan_api_info['tag']:
            clansFR[clan_api_info['clan_id']] = {
                'clan_tag': clan_api_info['tag'],
                'clan_name': clan_api_info['name']
            }
            print("SUCCESS")
        else :
            removed_clan.append(clan)
            print("FAILED, invalid clan name, probably missspelled")
    else :
        removed_clan.append(clan)
        print("FAILED, invalid clan name")


### Dumping data in files
current_date_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

print("=== Stats from data ===")
print(f"Added {len(extract_clean)-len(removed_clan)} new clans ")
print(f"Found {len(clansFR)} total clans ")
print(f"Added {len(removed_clan)} invalid clans")

print("=== Dumping data ===")
print("Dumping correct data with all available clans")
with open(f"{data_path}/{current_date_time}_french_clan_list.json", "w") as outfile:
    outfile.write(json.dumps(clansFR, indent=4))
    
output_removed = list(set(removed_clan+old_removed_clan))
print("Dumping data for unavailable clans")
with open(f"{output_path}/{current_date_time}_removed_clan.json", "w") as outfile:
    outfile.write(json.dumps(output_removed, indent=4))
