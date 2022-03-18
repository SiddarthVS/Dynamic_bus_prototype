import gspread
import pandas as pd


class gSheets:

    __studentlist = ('SEC21AD010', 'SIT21AD011', 'SIT20AD007', 'SIT21AD054',
                     'SIT20AD013', 'SIT20AD041', 'SEC19EC174', 'E8CS029')

    def __init__(self):
        # Call API and access file
        self.sheet_acc = gspread.service_account(filename="sairam-bus-records-735efd54fdc0.json")
        self.sheet_open = self.sheet_acc.open("LOG")
        # Open Sheet and convert to data frame
        self.sheet = self.sheet_open.worksheet("Sheet1")

    def student(self, iteratinglist):
        invalid_users = []
        for ind in range(len(iteratinglist)):
            stu_id = iteratinglist.iloc[ind, 0]
            if stu_id not in self.__studentlist and stu_id not in invalid_users:
                invalid_users.append(stu_id)
        return invalid_users

    def main(self):
        df = pd.DataFrame(data=self.sheet.get_all_values())
        college_id = df.iloc[1:5, [2]]
        unauthorized_student = self.student(college_id)
        print(unauthorized_student)

    def clear_sheet_on_time(self):
        pass


in_sheet = gSheets().main()
