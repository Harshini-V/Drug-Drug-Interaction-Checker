# Workflow for preprocessing

# First, extract data from the drugbank xml file (database)
# Inputs: dB_file = 'full_database.xml'
# Outputs: saveFile = 'extracted_full.csv'
python extract_db.py
# the output has all the drugs, plus synonym, classification, drug interactions, pathways, and targets

# Then, extract only the names from the drugbank database - for reference later
# Inputs: dB_file = 'full_database.xml'
# Outputs: saveFile = 'ids_and_names.csv'
python get_idname.py

# From these previous outputs, extract and reformat data
# Inputs: drug_ids_names_file = 'ids_and_names.csv', 'extracted_full.csv'
# Output: final_file = 'extract_list_final.csv'
python fix_csv.py
# Output in this format:  drug_id_1, drug_name_1, drug_id_2, drug_name_2, interaction description

# Find all drug pairs without any interactions between them
# Inputs: all_drugs_file = 'ids_and_names.csv', interactions_file = 'extract_list_final.csv'
# Output: output_file = 'no_interaction_pairs.csv'
python get_no_int_pairs.py
# Output is the same as the last output, but without the list of interactions (since there are none)

# Compiling general drugs and SMILES data
# Meghna generated SMILES data using 'get_smiles_data.ipynb'
# Inputs: drug_list = 'ids_and_names.csv', smiles_drug_list = 'SMILES_per_drugID.csv'
# Outputs: 'drugs_init_and_smiles.csv', 'drugs_without_smiles.csv'
python drug_and_smiles.py
# Outputs 2 files with the drug id, name, and smiles (if appl.) - one for those with smiles data, and one without

# SPECIAL CASES

# Filter for specific drugs in output
# In this case, we want only a certain list of OTC drugs (common), found in 'otc_generic_names.txt'
# Inputs: csv_file = 'extract_list_final.csv', drug_list = 'otc_generic_names.txt'
# Output: output_file = 'filtered_extract_list_otc.csv'
python filter_otc_drugs.py
# Output is basically a mini version of the full extracted list
# Other runs:
    # 1: in no interaction pairs getting only generic otc drugs
    # csv_file = 'no_interaction_pairs.csv'
    # drug_list = 'otc_generic_names.txt'
    # output_file = 'no_interaction_pairs_otc_only.csv'

    # 2: filter for both desired otc and prescription drugs (from filtered otc list)
    # csv_file = 'filtered_extract_list_otc.csv'
    # drug_list = 'unique_generic_names.txt'
    # output_file = 'filtered_extract_list_both.csv'

    # 3: filter for both desired otc and prescription drugs without interactions (from filtered otc list)
    # csv_file = 'no_interaction_pairs_otc_only.csv'
    # drug_list = 'unique_generic_names.txt'
    # output_file = 'filtered_no_interaction_pairs.csv'
