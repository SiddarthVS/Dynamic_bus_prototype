import gspread
import pandas as pd
import datetime
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

unique_passengers = []
date = datetime.datetime.now().strftime("%B %d,%Y")
list_len = 0

class upLoad:

    def __init__(self):
        # Call API and access file
        self.sheet_acc = gspread.service_account(filename="sairam-bus-records-735efd54fdc0.json")
        self.sheet_open = self.sheet_acc.open("LOG")
        # Open Sheet and convert to data frame
        self.sheet = self.sheet_open.worksheet("Sheet1")

    def read_records(self):
        # Append in list from sheets
        list_change_flag = 0
        global list_len
        df = pd.DataFrame(data=self.sheet.get_all_values())
        college_id = df.iloc[0:, [2]]
        for i, j in college_id.iterrows():
            s = str(j.iloc[list_len])
            if s not in unique_passengers:
                unique_passengers.append(s)
        if len(unique_passengers) > list_len:
            list_len = len(unique_passengers)
            list_change_flag = 1
        print(unique_passengers, date, list_len)
        self.load_record(unique_passengers, list_change_flag)

    def load_record(self, passenger_list, flag):
        global date
        # Use the application default credentials
        cred = credentials.Certificate("sairam-bus-records-firebase-adminsdk-satmc-89b99116c7.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        # db is the database variable

        # Upload Code
        data = {
            u'Year1': 1,
            u'Year2': 1,
            u'Year3': 1,
            u'Year4': 1,
            u'Strength': len(passenger_list)+1,
            u'Category': 5
        }

        # Add a new doc in collection or modify if existing
        up = db.collection(u'Strength Log').document(f'{date}')
        up.set(data, merge=True)

        # Below code for getting the data from firestore
        count_ref = db.collection(u'Strength Log')
        doc = count_ref.where(u'Category', u'==', 1).get()
        strength = []
        for document in doc:
            strength.append(document.to_dict())
        print(strength)

upLoad().read_records()
