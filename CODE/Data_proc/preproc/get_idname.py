"""
TITLE :parsing_DrugBank
AUTHOR : Hernansaiz Ballesteros, Rosa.
            rosa.hernansaiz@bioquant.uni-heidelberg.de
DESCRIPTION : Parsing full database of DrugBank to extract information
                about drugs that affects a specific organism.
                Information retrieved:
                    - name
                    - synonyms
                    - classification (kingdom and superfamily)
                    - drug-interactions (with other drugs)
                    - external-identifiers (to connect to other sources)
                    - pathways
                    - targets (if polypeptides)
                        - target_name
                        - target_uniprot
                        - target_gene_name
                        - action (of the drug over the target)
                        - cell_loc (cell localitation)
              To get the tree structure of the xml file,
                see drugBank_tree_structure.txt
LICENSE : GPL-v3
URL: https://gist.github.com/rosherbal/56461421c69a8a7da775336c95fa62e0
"""
# Parameters and required variables #

#dB_file = '../00-Drugs/drugBank_v515_20200103.xml'
dB_file = 'full_database.xml'
organism = 'Humans'
saveFile = 'ids_and_names.csv'

# Main script #
'''
Get targets from drugBank database for the drugs on the ic50 file
'''

import xml.etree.ElementTree as ET
import time
from tqdm import tqdm
import pandas as pd

xtree = ET.parse(dB_file)
xroot = xtree.getroot()
drugs = list(xroot)

drug_targets = []
for i in tqdm(range(len(drugs))):
    drug = drugs[i]
    idDB = drug[0].text # Drug Bank ID

    # Loop through features to find drug name
    drug_name = None
    for feature in drug:
        if 'name' in str(feature):
            drug_name = feature.text
            break  # Exit loop once name is found

    # Store the ID and name in a dictionary
    drug_dict = {
        "dg_id": idDB,
        "dg_name": drug_name
    }
    drug_targets.append(drug_dict)

# Convert to DataFrame and save to CSV
dt = pd.DataFrame(drug_targets)
dt.to_csv(saveFile, index=False)
print(f"Extracted data saved to {saveFile}")

 