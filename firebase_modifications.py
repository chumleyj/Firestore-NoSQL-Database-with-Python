import pandas as pd
from google.cloud.firestore import Client

full_file = 'Resources\\full_einstein_25col.csv'
reduced_file = 'Resources\\full_einstein_25col_reduced.csv'

# This function uploads a patient document to the firestore 
# collection indicated in the parameter
def upload_patient(patient_data, collection_name):
    
    # check for an existing patient document with the same ID
    db = Client()
    doc = db.collection(collection_name).document(patient_data['ID']).get()

    if doc.exists:
        print('\nA patient with this identifier already exists. Create a new unique ID and resubmit.\n')
    else:
        db.collection(collection_name).document(patient_data['ID']).set(patient_data)

# This function deletes a patient document from the collection 
# indicated in the parameter
def delete_patient(patient_id, collection_name):
    
    db = Client()
    doc = db.collection(collection_name).document(patient_id).get()

    if doc.exists:
        db.collection(collection_name).document(patient_id).delete()
    else:
        print('\nNo patient with this identifier exists.\n')

# This function edits the data in a patient document in the collection
# indicated in the parameter
def modify_patient(patient_data, collection_name):
    
    db = Client()

    doc = db.collection(collection_name).document(patient_data['ID']).get()

    if doc.exists:
        
        # convert existing data to dictionary
        entry = doc.to_dict()
        
        # loop through all keys in patient_data
        for key in patient_data.keys():
            
            # update patient data or nested CBC data
            if key == 'ID':
                continue
            elif key in entry.keys():
                entry[key] = patient_data[key]
            elif key in entry['CBC'].keys():
                entry['CBC'][key] = patient_data[key]
        
        db.collection(collection_name).document(patient_data['ID']).set(entry)
    else:
        print('\nNo patient exists with the given ID.\n')
    
# This function uploads all data from the file to firestore. Each test result
# is created as a document.
def upload_test_results_to_firestore(collection_name):
    # import csv data file and perform basic data cleanup
    covid_cbc_df = pd.read_csv(reduced_file, header=0, parse_dates=['Date'])
    covid_cbc_df.rename(columns={'y': 'COVID', 'Leukocytes':'WBC', 'RedBloodCells': 'RBC', 'Platelets':'PLT'}, inplace=True)
    covid_cbc_df['COVID'].replace({0: 'No', 1: 'Yes'}, inplace=True)

    # set firestore client (authentication handled outside of Python)
    db = Client()

    # create documents in firestore for each patient
    for i in covid_cbc_df.index:
        data = covid_cbc_df.iloc[i, 0:5].to_dict()
        data['CBC'] = covid_cbc_df.iloc[i, 5:].to_dict()
        db.collection(collection_name).document(data['ID']).set(data)

# This function gets all of the column names from a dataset and prompts
# the user for units for each column, then uploads then to either a 
# patient or CBC document in firestore
def upload_test_units_to_firestore():
    # import csv data file and perform basic data cleanup
    covid_cbc_df = pd.read_csv(full_file, header=0, parse_dates=['Date'])
    covid_cbc_df.rename(columns={'y': 'COVID', 'Leukocytes':'WBC', 'RedBloodCells': 'RBC', 'Platelets':'PLT'}, inplace=True)

    # set firestore client (authentication handled outside of Python)
    db = Client()

    # create list of column names
    col_names = list(covid_cbc_df.columns)
    cbc_units = {}
    patient_units = {}
    
    # loop through each column, prompting the user for a unit.
    for i in range(0, len(col_names)):
        user_input = input(f'Units for {col_names[i]}: ')
        
        # assign Age, COVID, ID, and Sex to patient, others to CBC
        if (col_names[i] in ['Age', 'COVID', 'ID', 'Sex']):
            patient_units[col_names[i]] = user_input
        else:
            cbc_units[col_names[i]] = user_input

    # upload to firestore
    db.collection(u'TestUnits').document('CBC').set(cbc_units)
    db.collection(u'TestUnits').document('Patient').set(patient_units)
