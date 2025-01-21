import os
import subprocess
import pandas as pd

batch_size = 1000
output_dir = "faers_results"
os.makedirs(output_dir, exist_ok=True)

# Load the total number of pairs
df_subset = pd.read_csv("./batch/predict_pairs.csv")
subset_pairs = list(zip(df_subset['Drug_Name_1'], df_subset['Drug_Name_2']))

total_batches = (len(subset_pairs) + batch_size - 1) // batch_size # Calculate number of batches run

for batch_index in range(total_batches):
    output_file = os.path.join(output_dir, f"batch_{batch_index}_features.csv")
    
    # Skip already processed batches
    if os.path.exists(output_file):
        print(f"Batch {batch_index} already processed. Skipping...")
        continue

    # Run the batch processing script
    print(f"Running batch {batch_index}...")
    subprocess.run(["python", "get_features_faers.py", str(batch_index)])

print("All batches processed.")
