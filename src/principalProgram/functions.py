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

class SaveExel:
    def __init__(self):
        self._index = 0

    def save_one(self, _row, _quantity, _wb, _file):
        self._index = 2
        for _cell in _row[-self._index::]:
            _cell.value = _quantity
            _wb.save(_file)
            return True

    def save_two(self, _row, _quantity, _time, _wb, _file):
        self._index = 21
        for _cell in _row[-self._index::]:
            print(_cell)
            _cell.value = _quantity
            _wb.save(_file)
            break

        for _cell_two in _row[-self._index+1::]:
            _cell_two.value = _time
            _wb.save(_file)
            break

    def save(self, _file, _sheet, _column, _name, quantity, _time):
        self._index = 0
        wb = load_workbook(_file)
        ws = wb[_sheet]
        column = ws[_column]
        for cell in column:
            if cell.value is not None and cell.value == _name:
                _row = ws[cell.row]
                if _file == "docx/docxxx1.xlsx":
                    SaveExel.save_one(self, _row, quantity, wb, _file)

                if _file == "docx/docxxx2.xlsx":
                    SaveExel.save_two(self, _row, quantity, _time, wb, _file)

                if _file == "docx/docxxx3.xlsx":
                    pass

        print("Listo")

    def action_save(self, _name, _quantity, _time):
        list_name = _name
        list_file = ["docx/docxxx1.xlsx", "docx/docxxx2.xlsx", "docx/docxxx3.xlsx"]
        list_sheet = ['MMQ  HOSPITAL ', 'MATERIA MQ', 'CONSOLIDADO MMQ']
        list_column = ['A', 'B', 'B']
        clean_sheet = 'MATERIAL DE ASEO-LIMPIEZA '

        for index in range(3):
            self.save(list_file[index], list_sheet[index], list_column[index], list_name[index], _quantity, _time)

if __name__ == '__main__':
    try:
        time = datetime.today()
        convert_time = datetime.strptime(str(time.date()), "%Y-%m-%d").date()
        prueba = SaveExel()
        nombres = ["ADHESIVO", "ADHESIVO", "epa"]
        prueba.action_save(nombres, 12, convert_time.strftime(format="%d/%m/%Y"))
    except Exception as e:
        print(f"ERRORES :: {e}")