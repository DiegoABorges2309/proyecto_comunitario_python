import datetime
from datetime import datetime

class Functions:
    def __init__(self):
        pass

    def group_list(self, c_list):
        for index in range(5):
            if c_list[index] == '':
                c_list[index] = None
        if c_list[1] != None:
            c_list[1] = float(c_list[1])

        if c_list[4] != None:
            c_list[4] = datetime.strptime(c_list[4], "%Y-%m-%d").date()

        return c_list