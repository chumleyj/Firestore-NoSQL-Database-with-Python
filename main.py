# Author: Jeffrey Chumley
# Date: 1/19/2022
# Description: This program analyzes a dataset of COVID-19
#  and CBC test results stored in a Firestore database.
#  Displays plots and statistical tests of the data.
#  See README.md file.

# import data analysis functions
from firebase_queries import query_cbc_analytes, query_patient_cbc_fields, query_summary
from firebase_modifications import delete_patient, modify_patient, upload_patient
from data_analysis_functions import *

# This function displays the menu options in menu_list
def display_menu(menu_list):
    print("\nMenu options: ")
    i = 1
    for option in menu_list:
        print(f'{i}. {option}')
        i += 1
        
# This function gets a menu selection from the user
def get_menu_selection(menu_list):
    
    selection = None

    # prompt for selection until valid one is received
    while selection not in range(1, len(menu_list) + 1):
        display_menu(menu_list)
        selection = int(input("Select an option: "))

        # notify of invalid input
        if selection not in range(1, len(menu_list) + 1):
            print("\nInvalid selection.\n")
    
    return (selection - 1)

# This function displays each key in fields_dict.
def display_analytes(analytes_dict):
    print("\nAnalytes: ")
    i = 1
    for key in sorted(analytes_dict.keys()):
        print(f'{i}. {key}')
        i += 1

# This function gets a field/analyte selection from the user
def get_analyte_selection(analytes_dict):

    selection = None

    # prompt for field selection until valid one is received
    while selection not in analytes_dict.keys():
        display_analytes(analytes_dict)
        selection = input("Select an analyte (type name): ")

        # notify of invalid input
        if selection not in analytes_dict.keys():
            print('\nInvalid selection\n')
    
    return selection

# This function prompts the user for all information to create 
# a new patient entry and returns the data as a dictionary
def prompt_patient_entry(patient_fields):
    
    new_patient = {'CBC': {}}

    # loop through all keys in patient fields and prompt for input
    for key in sorted(patient_fields.keys()):
        if (key == 'Age'):
            new_patient[key] = int(input(f'Input {key}: '))
        elif (key != 'CBC'):
            new_patient[key] = input(f'Input {key}: ')
        elif (key == 'CBC'):
            for cbc_key in sorted(patient_fields['CBC'].keys()):
                new_patient['CBC'][cbc_key] = int(input(f'Input {cbc_key}: '))

    return new_patient

# This fucntion prompts the user for a patient and value to update
def prompt_modify_value(patient_fields):
    
    id = input('Enter a patient ID: ')
    field_name = get_analyte_selection(patient_fields['CBC'])
    
    while (field_name == 'ID'):
        print('Cannot modify the patient ID.')
        field_name = get_analyte_selection(patient_fields['CBC'])
    
    value = int(input('Enter the new value: '))

    return {field_name: value, 'ID': id}


# dictionaries to hold figures and statistics from previous
# queries to reduce redundant queries to firestore. Initializes
# keys for each CBC analyte but no values
analyte_figs = query_cbc_analytes()
median_stats = query_cbc_analytes()
cbc_data_summary = None
patient_fields = None

# list of menu options to display
menu_list = ('Plot CBC Analyte by COVID',
             'Compare CBC Analyte Median by COVID',
             'Summary of the dataset',
             'Add patient',
             'Modify patient',
             'Delete patient',
             'Clear locally stored data',
             'Exit'
)

# prompt user for what to display
menu_selection = 0

# continue showing options and results until user quits
while (menu_selection >= 0 and menu_selection < len(menu_list)):
    
    menu_selection = get_menu_selection(menu_list)

    # menu_list[0]
    if (menu_selection == 0):
        # get analyte selection from user
        analyte_selection = get_analyte_selection(analyte_figs)
        
        # if figure for analyte not stored, query firestore for data and display
        if analyte_figs[analyte_selection] == None:
            analyte_figs[analyte_selection] = plot_analyte_by_covid(analyte_selection)
        # if figure stored from previous query, redisplay figure
        else:
            print('\nRe-displaying previously generated plot.\n')
            redisplay_fig(analyte_figs[analyte_selection])
    
    # menu_list[1]
    elif (menu_selection == 1):
        # get analyte selection from user
        analyte_selection = get_analyte_selection(median_stats)
        
        # if statistic for analyte not stored, query firestore for data
        if median_stats[analyte_selection] == None:
            median_stats[analyte_selection] = compare_analyte_by_covid(analyte_selection)
        else:
            print('\nRe-displaying previously calculated statistic.\n')
        
        # display statistics
        display_statistic(median_stats[analyte_selection])
    
    # menu_list[2]
    elif (menu_selection == 2):
        
        # if cbc_data_summary is empty, query summary data
        if (cbc_data_summary == None):
            cbc_data_summary = query_summary()
        
        # display summary
        display_summary(cbc_data_summary)
        
    # menu_list[3]
    elif (menu_selection == 3):
        
        # check if all required fields have already been queried and stored locally
        if (patient_fields == None):
            patient_fields = query_patient_cbc_fields()
        
        # prompt user for new patient data and upload that data to the database
        new_patient = prompt_patient_entry(patient_fields)
        upload_patient(new_patient, 'TestResults2')

    # menu_list[4]
    elif (menu_selection == 4):
        
        # check if all required fields have already been queried and stored locally
        if (patient_fields == None):
            patient_fields = query_patient_cbc_fields()
        
        # prompt user for value to modify then modify it
        modify_value = prompt_modify_value(patient_fields)
        modify_patient(modify_value, 'TestResults2')
    
    # menu_list[5]
    elif (menu_selection == 5):
        id = input('Enter a patient ID to delete from the database: ')
        delete_patient(id, 'TestResults2')

    # menu_list[6]
    elif (menu_selection == 6):
        # clear locally stored figures, statistics, and summary
        analyte_figs = query_cbc_analytes()
        median_stats = query_cbc_analytes()
        cbc_data_summary = None
        patient_fields = None
        print('\nLocally stored data has been removed. Requests will be refreshed from the database.\n')

    # exit loop
    else:
        menu_selection = len(menu_list)