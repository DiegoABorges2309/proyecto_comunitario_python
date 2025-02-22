import datetime
from datetime import datetime
from openpyxl import load_workbook

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

class SaveExel():
    def __init__(self):
        self._index = 0

    def save_one(self, _row, _quantity, _wb, _file):
        self._index = 2
        for _cell in _row[-self._index::]:
            print(_cell.value)
            _cell.value = _quantity
            _wb.save(_file)
            return True

    def save_two(self, _row, _quantity, _wb, _file):
        self._index = 1
        for _cell in _row[-self._index::]:
            print(_cell.value)
            _cell.value = _quantity
            _wb.save(_file)
            return True

    def save(self, _file, _sheet, _column, _name, quantity):
        self._index = 0
        try :
            wb = load_workbook(_file)
            ws = wb[_sheet]
            column = ws[_column]
            for cell in column:
                if cell.value is not None and cell.value == _name:
                    _row = ws[cell.row]
                    if _file == "docx/docxxx1.xlsx":
                        SaveExel.save_one(self, _row, quantity, wb, _file)
                    elif _file == "docx/docxxx2.xlsx":
                        SaveExel.save_two(self, _row, quantity, wb, _file)
                    elif _file == "docx/docxxx3.xlsx":
                        pass
        except Exception:
            return False
