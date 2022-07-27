from firebase_admin import credentials
from firebase_admin import initialize_app
from firebase_admin import storage


class record:

    def __init__(self, string):
        cred = credentials.Certificate("sairam-bus-records-firebase-adminsdk-satmc-89b99116c7.json")
        initialize_app(cred, {'storageBucket': 'sairam-bus-records.appspot.com'})
        bucket = storage.bucket()
        data = bucket.list_blobs()
        req_file = ""
        for i in data:
            if string in i.name:
                req_file = i.name
                break
        if req_file == "":
            print("Record Not Found")
            return
        file = bucket.get_blob(req_file)
        print(file)
        try:
            # A file in the local directory should be specified similar to the file type and the file should be existing
            # The data is re-written in  the file mentioned
            file.download_to_filename("E:/Projects/Logistic Routing/Dynamic/Downloads/test.xls")

        except:
            print("Record Not Found")


# Change the value based on front-end input
record("2022-04-04")
