import csv
import sys

# Increase the CSV field size limit
csv.field_size_limit(sys.maxsize)

# Filter for specifc drugs

# file paths (examples)
# csv_file = 'extract_list_final.csv'
# drug_list = 'otc_generic_names.txt'
# output_file = 'filtered_extract_list_otc.csv'

# csv_file = 'no_interaction_pairs.csv'
# drug_list = 'otc_generic_names.txt'
# output_file = 'no_interaction_pairs_otc_only.csv'

# csv_file = 'filtered_extract_list_otc.csv'
# drug_list = 'unique_generic_names.txt'
# output_file = 'filtered_extract_list_both.csv'

csv_file = 'no_interaction_pairs_otc_only.csv'
drug_list = 'unique_generic_names.txt'
output_file = 'filtered_no_interaction_pairs.csv'

# read drug names from the text file
with open(drug_list, 'r') as file:
    names_in_text = set(line.strip() for line in file)

# read in CSV, check for matching drug names in columns 2 or 4, and write matching rows to new CSV
with open(csv_file, 'r') as csv_in, open(output_file, 'w', newline='') as csv_out:
    reader = csv.reader(csv_in)
    writer = csv.writer(csv_out)

    # write header to the output file
    header = next(reader)
    writer.writerow(header)

    for row in reader:
        # check if the drug name in the second or fourth column is in the names_in_text set
        if row[1] in names_in_text or row[3] in names_in_text:
            writer.writerow(row)  # write out
