import csv
from itertools import combinations

# File paths
all_drugs_file = 'ids_and_names.csv'            # CSV file with the list of all drugs
interactions_file = 'extract_list_final.csv'  # CSV file with all drug interactions (filtered)
output_file = 'no_interaction_pairs.csv'     # Output file for drug pairs with no interactions

# Step 1: Load all drug IDs and names
drug_info = {}  # Dictionary to store drug ID and name pairs
with open(all_drugs_file, 'r') as drugs_csv:
    reader = csv.reader(drugs_csv)
    next(reader)  # Skip the first row (header)
    for row in reader:
        drug_id = row[0]
        drug_name = row[1]
        drug_info[drug_id] = drug_name  # Map drug ID to drug name
matched = {}

drug_list = list(drug_info.items())

for i, (current_drug_id, current_drug_name) in enumerate(drug_list):
    
    # Check if there is a next drug
    if i < len(drug_list) - 1:
        # Get next drug details
        next_drug_id, next_drug_name = drug_list[i + 1]
        
        # add each match to dict
        matched[(current_drug_id, next_drug_id)] = (current_drug_name, next_drug_name)

# Step 2: Load existing interactions into a set of tuples
existing_interactions = set()
with open(interactions_file, 'r') as interactions_csv:
    reader = csv.reader(interactions_csv)
    for row in reader:
        # Store each pair as a tuple of (drug_id_1, drug_id_2)
        drug1, drug2 = row[0], row[2]  # Columns 0 and 2 are drug IDs in the interaction file
        # Ensure consistent ordering for pairs (drug1, drug2) and (drug2, drug1)
        existing_interactions.add(tuple(sorted((drug1, drug2))))

# Step 3: Find pairs with no interactions
no_interaction_pairs = []
# now search through all matches to find pairs without interactions
for i, pair in matched.items():
    if i not in existing_interactions:
        drug1, drug2 = i
        drug_name1, drug_name2 = pair
        # Append the pair including IDs and names
        no_interaction_pairs.append((drug1, drug_name1, drug2, drug_name2))

# Step 4: Write pairs without interactions to a new CSV file
with open(output_file, 'w', newline='') as output_csv:
    writer = csv.writer(output_csv)
    # Write header for the output file
    writer.writerow(['Drug_ID_1', 'Drug_Name_1', 'Drug_ID_2', 'Drug_Name_2'])
    # Write each pair with IDs and names
    writer.writerows(no_interaction_pairs)
