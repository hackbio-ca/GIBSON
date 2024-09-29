import requests
import pandas as pd
import os
import json

# Fetches RNA sequences from RNAcentral for a given organism, sequence length range, and sequence type.
# Stores each sequence as a json file. 

# the base url to fetch sequence
url = "https://rnacentral.org/api/v1/rna/"

# parameters to use in the query
parameters = {
    "taxon_id": 9606,  # H. sapiens
    "min_length": 100,  # Set the minimum length of RNA sequences
    "max_length": 200,  # Set max length to 200 nt, i.e., small noncoding RNAs
    "type": "sncRNA",  # small noncoding RNAs
    "format": "json",  # Use json format for results
    "page_size": 100  # get 100 results per page
}

# a list to store the RNA data
rna_data = []

# use cwd to make relative directory if it does not yet exist
relative_dir = './data_v2/json/'
os.makedirs(relative_dir, exist_ok=True)

# uses RNAcentral API to access data
response = requests.get(url, params=parameters)
data = response.json()

# Counter to track the total number of sequences saved
sequence_count = 0  

# Loop through the results and append to the list
while data:
    # Extract and store RNA data
    for entry in data['results']:
        
        rna_id = entry['rnacentral_id']  # Use the RNAcentral ID for the file name
        json_filename = f'{relative_dir}{rna_id}.json'  # Create a JSON file for each RNA sequence
        
        # Save the current sequence's response as a JSON file
        with open(json_filename, 'w') as json_file:
            json.dump(entry, json_file, indent=4)  # Save the JSON file
        
        print(f"Saved sequence {sequence_count + 1} with RNA ID: {rna_id} to {json_filename}")
        
        # Add the RNA entry to the list for CSV saving
        rna_data.append({
            "RNA_id": entry['rnacentral_id'],
            "seq": entry['sequence'],
            "length": entry['length']
        })
        
        sequence_count += 1  # Increment sequence count
    
    # Pagination: Get the next page of data if needed
    if data['next']:
        response = requests.get(data['next'])
        data = response.json()
    else:
        break  # Exit if no more pages are left to process

