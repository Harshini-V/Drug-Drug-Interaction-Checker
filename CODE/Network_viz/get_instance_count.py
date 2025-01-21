import os
import sys
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import requests

# Query FAERS API
def query_faers(pair):
    drug1, drug2 = pair
    query = f"patient.drug.medicinalproduct:{drug1}+AND+{drug2}"
    params = {"search": query, "limit": 200}
    try:
        response = requests.get("https://api.fda.gov/drug/event.json", params=params, timeout=10)
        if response.status_code == 200:
            return {"pair": pair, "data": response.json()}
    except requests.exceptions.RequestException as e:
        print(f"Error querying pair {pair}: {e}")
    return {"pair": pair, "data": None}

# Extract frequency from FAERS data
def extract_frequency(faers_data):
    frequency_count = 0
    if faers_data and 'results' in faers_data:
        for event in faers_data['results']:
            drugs = event.get("patient", {}).get("drug", [])
            if len(drugs) <= 3:  # Process only reports with <= 3 drugs
                frequency_count += 1
    return frequency_count

if __name__ == "__main__":
    # Get batch index from command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python process_batch.py <batch_index>")
        sys.exit(1)
    
    batch_index = int(sys.argv[1])
    batch_size = 1000
    output_dir = "faers_results"
    os.makedirs(output_dir, exist_ok=True)

    # Load dataset
    df_subset = pd.read_csv("drug_pairs.csv")
    subset_pairs = list(zip(df_subset['Drug_Name_1'], df_subset['Drug_Name_2']))

    # Split into batches
    batches = [subset_pairs[i:i + batch_size] for i in range(0, len(subset_pairs), batch_size)]

    # Check if batch_index is valid
    if batch_index >= len(batches):
        print(f"Invalid batch index {batch_index}. Only {len(batches)} batches available.")
        sys.exit(1)

    batch = batches[batch_index]
    output_file = os.path.join(output_dir, f"batch_{batch_index}_frequency.csv")
    
    # Skip already processed batches
    if os.path.exists(output_file):
        print(f"Batch {batch_index} already processed. Skipping...")
        sys.exit(0)

    print(f"Processing batch {batch_index}...")
    with ThreadPoolExecutor(max_workers=20) as executor:
        batch_results = list(tqdm(executor.map(query_faers, batch), total=len(batch), desc=f"Batch {batch_index}"))

    # Extract frequency for this batch
    batch_frequencies = []
    for result in batch_results:
        pair = result['pair']
        faers_data = result['data']
        freq = extract_frequency(faers_data)
        batch_frequencies.append({
            "Drug_Name_1": pair[0], "Drug_Name_2": pair[1],
            "Adverse_Event_Frequency": freq
        })

    # Convert to DataFrame and save
    df_batch_frequencies = pd.DataFrame(batch_frequencies)
    df_batch_frequencies.to_csv(output_file, index=False)
    print(f"Batch {batch_index} frequencies saved to {output_file}.")

