from google.cloud.firestore import Client

test_results_test = 'TestResults2' # reduced database size for testing
test_results = u'TestResults' # full database

# This function queries the CBC units document in firestore and 
# returns a dictionary with keys corresponding to each field.
# Value for each key is None.
def query_cbc_analytes():
    
    db = Client()
    cbc_doc = db.collection(u'TestUnits').document(u'CBC').get()

    # create dictionary with keys corresponding to each CBC analyte
    analytes = cbc_doc.to_dict()

    # set all values to None
    for key in analytes.keys():
        analytes[key] = None

    return analytes

# This function queries the TestUnits collection in firestore
# and returns a dictionary with keys corresponding to each
# data. Value for each key is None.
def query_patient_cbc_fields():

    db = Client()
    patient_doc = db.collection(u'TestUnits').document(u'Patient').get()

    patient_dict = patient_doc.to_dict()
    patient_dict['CBC'] = query_cbc_analytes()
    return patient_dict

# This function queries the CBC document in the TestUnits
# collection and returns the unit of measurement associated
# with the analyte parameter.
def query_cbc_analyte_unit(analyte):

    db = Client()

    doc = db.collection(u'TestUnits').document(u'CBC').get()
    units = doc.to_dict()

    return units[analyte]


# This function queries all TestResult documents in firestore
# and copies the result associated with the parameter analyte
# to a list based on whether the patient was COVID negative
# or COVID positive.
def query_cbc_analyte_by_covid(analyte):

    db = Client()

    # get documents in TestResults collection
    docs = db.collection(test_results_test).get()
    neg_list = []
    pos_list = []

    for doc in docs:
        entry = doc.to_dict()
        if (entry['COVID'] == 'No'):
            neg_list.append(entry['CBC'][analyte])
        elif (entry['COVID'] == 'Yes'):
            pos_list.append(entry['CBC'][analyte])
    
    return [neg_list, pos_list]


# This function queries the database to get the age,
# COVID status, and Sex of all patients
def query_summary():
    
    db = Client()

    docs = db.collection(test_results_test).get()
    summary = {'Age': [], 'COVID': [], 'Sex': []}
    for doc in docs:
        entry = doc.to_dict()
        summary['Age'].append(entry['Age'])
        summary['COVID'].append(entry['COVID'])
        summary['Sex'].append(entry['Sex'])
    
    return summary