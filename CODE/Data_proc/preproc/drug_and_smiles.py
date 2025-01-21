import csv

drug_list = 'ids_and_names.csv'
smiles_drug_list = 'SMILES_per_drugID.csv'


# Initialize dictionaries to hold drug data by ID
drug_names = {}
drug_smiles = {}

# Load drug names into dictionary
with open(drug_list, 'r') as name_file:
    reader = csv.reader(name_file)
    next(reader)  # Skip header if there is one
    for row in reader:
        drug_id, name = row
        drug_names[drug_id] = name

# Load drug SMILES codes into dictionary
with open(smiles_drug_list, 'r') as smiles_file:
    reader = csv.reader(smiles_file)
    next(reader)  # Skip header if there is one
    for row in reader:
        drug_id, smiles = row
        drug_smiles[drug_id] = smiles

# Open the output CSV file for writing
with open('drugs_init_and_smiles.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['ID', 'Name', 'SMILES'])  # Write header

    # Print header for console output
    print("ID, Name, SMILES")

    # Open another file for drugs only found in drug_names
    with open('drugs_without_smiles.csv', 'w', newline='') as missing_file:
        missing_writer = csv.writer(missing_file)
        missing_writer.writerow(['ID', 'Name'])  # Write header for drugs without SMILES

        # Find drugs with both name and SMILES data, print and write them to file
        for drug_id in drug_names:
            if drug_id in drug_smiles:
                name = drug_names[drug_id]
                smiles = drug_smiles[drug_id]
                
                # Write to CSV file for matched drugs
                writer.writerow([drug_id, name, smiles])
                
                # Print to console
                print(f"Matched - ID: {drug_id}, Name: {name}, SMILES: {smiles}")
            else:
                # Write to CSV file for drugs without SMILES
                name = drug_names[drug_id]
                missing_writer.writerow([drug_id, name])
                
                # Print to console
                print(f"Unmatched - ID: {drug_id}, Name: {name} (No SMILES code)")
