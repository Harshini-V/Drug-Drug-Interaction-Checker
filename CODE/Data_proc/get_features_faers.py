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

# Extract features from FAERS data
def extract_features(faers_data):
    frequency_count = 0
    severity_score = 0
    if faers_data and 'results' in faers_data:
        for event in faers_data['results']:
            drugs = event.get("patient", {}).get("drug", [])
            if len(drugs) <= 3:  # Process only reports with <= 3 drugs
                frequency_count += 1
                seriousness = {
                    "hospitalization": event.get("seriousnesshospitalization"),
                    "disability": event.get("seriousnessdisabling"),
                    "life_threatening": event.get("seriousnesslifethreatening"),
                    "death": event.get("seriousnessdeath")
                }
                severity_score += (
                    (int(seriousness.get("hospitalization") or 0) * 1) +
                    (int(seriousness.get("disability") or 0) * 2) +
                    (int(seriousness.get("life_threatening") or 0) * 3) +
                    (int(seriousness.get("death") or 0) * 5)
                )
    return frequency_count, severity_score

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
    df_subset = pd.read_csv("./batch/predict_pairs.csv")
    subset_pairs = list(zip(df_subset['Drug_Name_1'], df_subset['Drug_Name_2']))

    # Split into batches
    batches = [subset_pairs[i:i + batch_size] for i in range(0, len(subset_pairs), batch_size)]

    # Check if batch_index is valid
    if batch_index >= len(batches):
        print(f"Invalid batch index {batch_index}. Only {len(batches)} batches available.")
        sys.exit(1)

    batch = batches[batch_index]
    output_file = os.path.join(output_dir, f"batch_{batch_index}_features.csv")
    
    # Skip already processed batches
    if os.path.exists(output_file):
        print(f"Batch {batch_index} already processed. Skipping...")
        sys.exit(0)

    # Parallelization
    print(f"Processing batch {batch_index}...")
    with ThreadPoolExecutor(max_workers=20) as executor:
        batch_results = list(tqdm(executor.map(query_faers, batch), total=len(batch), desc=f"Batch {batch_index}"))

    # Extract features for this batch
    batch_features = []
    for result in batch_results:
        pair = result['pair']
        faers_data = result['data']
        freq, severity = extract_features(faers_data)
        batch_features.append({
            "Drug_Name_1": pair[0], "Drug_Name_2": pair[1],
            "Adverse_Event_Frequency": freq, "Severity_Score": severity
        })

    # Convert to DataFrame and save
    df_batch_features = pd.DataFrame(batch_features)
    df_batch_features.to_csv(output_file, index=False)
    print(f"Batch {batch_index} features saved to {output_file}.")
