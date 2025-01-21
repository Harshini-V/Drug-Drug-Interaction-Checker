Group 23 Compiled README file. Each respective folder in CODE has its own README, relaying the exact same information here.

GENERAL DATA PROCESSING:
We had 3 datasets we pulled from: DrugBank, DDInter, and FAERS.
DrugBank required an academic license to access, and was downloadable after obtaining from the DrugBank website: https://go.drugbank.com/releases/latest. It was a relatively large XML file, with over 8GB of data after unzipping. It was also hard to extract data from, and required modifying a script found online to obtain data.
Extracting DDInter data is expanded on in Network Visualization section.
FAERS data was extracted using API calls. Due to the number of calls and time required, we batched the calls to make it easier. In total, we extracted only a few MB of data. This is open source data. 
We used a lot of helper code to extract data from various outputs and combine them, creating a lot of output files in various formats for ease of use in our code. Some of these are not included, as they are numerous and simple. Some are included, in their own folder under Data_proc, called preproc. This folder contains a file called preprocessing_workflow_drugbank.sh, which outlines how to use all the files.

Most of the data processing was compiled into one Jupyter Notebook, for ease of use and explanation.
FILES:
compiled_data_proc.ipynb:
Usage: Gets features for the ML model. Calculates Jaccard Similarity (for protein targets), gets the SMILES data for Tanimoto Correlation (calculated in ML code). Combines all the extracted data (features) needed to test, train, and run the ML model.
Input: feature data from FAERS, drug pairs with target names, SMILES sdf file, [OPTIONAL] label data for testing ML model effectiveness
Output: jaccard_similarity.csv (also used as input), SMILES_per_drugID.csv (SMILES data for each drug), data_with_features.csv or data_with_features_and_label.csv (all compiled features)

extract_db.py:
Usage: Pulls data from DrugBank XML file. Based on script: https://gist.github.com/rosherbal/56461421c69a8a7da775336c95fa62e0
This was slightly modified to obtain desired data.
Input: drug_bank.xml
Output: Large csv file with all drugs, plus synonym, classification, drug interactions, pathways, and targets.

FAERS Data Extraction:
This was done using two scripts, get_features_faers.py, and batch_run.py.
batch_run.py:
Usage: Runs batches of the specified amount (in this case 1000) to call the FAERS API. It calls get_features_faers.py, which is what actually calls and outputs the data, using a subprocess.
Input: Prediction pairs
Output: Files of all the specified drug pairs, each with the counted number of adverse events, and the severity level of those adverse events. Split up by batch, but can be easily catted together: cat faers_results/* >> output.csv

get_features_faers.py:
Usage: Calls FAERS API, and counts the number of adverse events reported between a drug pair, then calculates a severity score based on how severe these events are (eg, hospitalization, death, etc).
Input: Prediction pairs
Output: File of all the specified drug pairs, each with the counted number of adverse events, and the severity level of those adverse events.


NETWORK VISUALIZATION:
The d3 visualization first shows a drop down menu, which allows users to search for a drug of interest. After choosing a drug, press the search button, and a network visualization will appear. This visualization shows the top 10 (or fewer if there were less interactions) interactions of that drug and other drugs reported in our dataset. There is also a predict button, which allows the user to interact with our ML model, predicting interactions that are either new or not found in our datasets. There are mouseover features which provide additional information about the interactions, including the severity, type, and likelihood of interaction for the predicted nodes.
FILES:
dva_json.py: 
usage: Compile all the data into json files to create nodes and edges that are used to build the visualization network
input: DDInter data accessible from https://ddinter.scbdd.com/download/, count output generated through count_batch_run.py and get_instance_count.py, predict file prediction_final.csv generated through ML model
output: two json files, graph_structure_final.json and graph_structure_predict_final.json

get_instance_count.py:
usage: runs drug pairs through the FAERS API and returns the number of instances (API key optional)
input: drug_pairs.csv, made a csv with all the drug pairs from DDInter
Output: none used in count_batch_run.py

count_batch_run.py:
usage: batches the usage of the API so that it doesn't time out
input: drug_pairs.csv and get_instance_count.py
output: count_output.csv, contains the drug pairs with their instance count

network_final.html:
usage: creates the network using the json files and implements all the visualizations
input: graph_structure_final.json and graph_structure_predict_final.json
output: can be visualized on the html server and interacted with

ML MODEL:
This jupyter notebook is divided into sections using Markdown cells.

- Data Preprocessing - Labels
usage: Adding labels to the drug pairs interaction data (1) and drug pairs no interaction data (0)
input: no_interaction_pairs.csv, extract_list_final.csv
output: df_combined - a dataframe that has all the drug pairs data with labels
        df_positive - a dataframe that has all the drug pairs with an interaction labelled 1
        df_negative - a dataframe that has all the drug pairs with no iteractions labelled 0

- Feature Engineering
    - Getting SMILES codes for each drug
    usage: adding the corresponding SMILES code for each drug
    input: drugs_init_and_smiles.csv, df_positive, df_negative
    output: df_negative and df_posiitves have SMILES codes.

    - Getting Samples Subset (100k)
    usage: creating a subset dataset of 100k instances of combined drug pair interaction and no interaction data and splitting it into two files of 50k each.
    input: df_negative, df_positive, df_combined
    output: subset_part1.csv - 50k instances of shuffled drug pairs and corresponding labels
            subset_part2.csv - 50k instances of shuffled drug pairs and corresponding labels

    - Calculating Chemical Similarity
    usage: These cells of code generates molecular finger prints using SMILES codes and calculates tanimoto similarity, then visualizes summary statistics as a histogram.
    input: subset_part1.csv
    output: subset_with_tan_sim.csv - drug pairs with corresponding tanimoto similarities
            subset_part1_with_fingerprints.pkl - pickle file saving the molecular finger prints of each drug
            tc_plot.png - histogram 

    - Extracting FAERS Data
    usage: These cells query faers API and calculate severity scores and adverse event frequency in batches of 1000, then merges the dataframe with all features.
    input: df_subset, filtered_jaccard_similarity_filled_all.csv
    output: faers_features_with_scores_5500_6500.csv
            subset_with_tan_sim.csv - drug pairs with corresponding tanimoto similarity scores
            faers_features_combined.csv - drug pairs with corresponding severity scores and adverse event frequency
            merged_features_similarity.csv - intermediate file with some merged features but not all
            merged_features_with_protein_target_scores.csv - drug pairs with protein target similarity scores
            combined_data - dataframe that has drug pairs, features, and labels ready for ML implementation (Class 1: 34798, Class 0:3940)


- Random Forest Implementation
    - Train Test Split
    usage: splits data into train validation test sets
    input: combined_data 
    - Fitting, Training, Testing (Hyperparameters Not Tuned)
    - Random Search (Hyperparameter Tuning)
    - Calibration and Final Model Evalauation
    output: random_forest_model_calibrated_best_params_64.pkl - saved best rf file
    - Plots
    output: confusion_matrix_rf_64_calibrated.png - confusion matrix
            feature_importance_64_calibrated.png - feature importance plot
- Predicting Interactions between OTC-prescription drug pairs using best RF model
usage: predicting drug pairs using best rf model
input: random_forest_model_calibrated_best_params_64.pkl - saved best rf model
output: prediction_scores_calibrated_64_bestparams.csv - drug pairs with probability scores

