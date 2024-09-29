import requests
import pandas as pd
import os


# the base url to fetch sequence
url = "https://rnacentral.org/api/v1/rna/"

# parameters to use in the query
parameters = {
    "taxon_id": 9606,  # H. sapiens
    "min_length": 100, # Set the min length
    "max_length": 200,  # Set max length to 200 nt, i.e., small noncoding RNAs.
    "type": "sncRNA",  # small noncoding RNAs
    "format": "json",  # Use json format for results
    "page_size": 100  # get 100 results per page
}

# a list to store the RNA data
rna_data = []

# uses RNAcentral API to access data.
response = requests.get(url, params=parameters)
data = response.json()

# Loop through the results and append to the list
while data:
    for entry in data['results']:
        rna_data.append({
            "RNA_id": entry['rnacentral_id'],
            "seq": entry['sequence'],
            "length": entry['length']
        })
    
    # pagination; use to get next page
    if data['next']:
        response = requests.get(data['next'])
        data = response.json()
    else:
        break  # exit if no pages left to parse

relative_dir = './output/'

# use cwd to make relative directory if it does not yet exist
os.makedirs(relative_dir, exist_ok=True)

# make a df out of the RNA data.
df = pd.DataFrame(rna_data)

# save the file as a csv

df.to_csv('./output/human_sncRNAs.csv', index=False)

print("Data has been saved to human_sncRNAs.csv")