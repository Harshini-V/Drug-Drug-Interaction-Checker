import csv
import sys

# Increase the CSV field size limit
csv.field_size_limit(sys.maxsize)

def initial(input_file, temp_output_file):
    # First function to create a temporary output file
    with open(input_file, 'r') as infile, open(temp_output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write header to output file
        writer.writerow(['dg_id1', 'dg_name1', 'dg_id2', 'Description'])

        # Iterate over each row in the CSV file
        next(reader)  # Skip the header row if it exists
        for row in reader:
            drug_id_1 = row[1]
            drug_name_1 = row[2]
            drug_ids_2 = row[6].split(';')
            int_descriptions = row[7].split(';')

            # Iterate through each item in columns 6 and 7
            for drug_id_2, int_description in zip(drug_ids_2, int_descriptions):
                writer.writerow([drug_id_1, drug_name_1, drug_id_2, int_description])

def load_drug_id_to_name(drug_ids_names_file):
    # Create a dictionary to map drug IDs to their names
    drug_id_to_name = {}
    with open(drug_ids_names_file, 'r') as id_name_file:
        reader = csv.reader(id_name_file)
        next(reader)  # Skip the header if it exists
        for row in reader:
            drug_id = row[0]
            drug_name = row[1]
            drug_id_to_name[drug_id] = drug_name
    return drug_id_to_name

def add_drug_name_2(temp_output_file, final_output_file, drug_id_to_name):
    # Read the temporary output file and write the final output file
    with open(temp_output_file, 'r') as temp_infile, open(final_output_file, 'w', newline='') as final_outfile:
        reader = csv.reader(temp_infile)
        writer = csv.writer(final_outfile)

        # Write new header with 'dg_name2' column
        writer.writerow(['dg_id1', 'dg_name1', 'dg_id2', 'dg_name2', 'Description'])

        # Iterate over each row in the temporary file and add 'dg_name2'
        next(reader)  # Skip the header row if it exists
        for row in reader:
            drug_id_1 = row[0]
            drug_name_1 = row[1]
            drug_id_2 = row[2]
            description = row[3]
            
            # Lookup the name for drug_id_2
            drug_name_2 = drug_id_to_name.get(drug_id_2, "Unknown")

            # Write only if drug_id_2 is non-empty or drug_name_2 is not "Unknown"
            if drug_id_2 or drug_name_2 != "Unknown":
                writer.writerow([drug_id_1, drug_name_1, drug_id_2, drug_name_2, description])

# Workflow
temp_file = 'extract_list_temp.csv'
final_file = 'extract_list_final.csv'
drug_ids_names_file = 'ids_and_names.csv'

initial('extracted_full.csv', temp_file)
drug_id_to_name = load_drug_id_to_name(drug_ids_names_file)
add_drug_name_2(temp_file, final_file, drug_id_to_name)
