import asyncio
from src.db.models import Users, Items, Exel

class UserLogin():
    def __init__(self):
        pass

    async def add_user(self, _user_name: str, _password: str):
        try:
            await Users.create(user_name=_user_name, password=_password)
            return True
        except Exception as e:
            return False

    async def verific_user(self, _user_name: str, _password: str):
        try:
            result = await Users.filter(user_name=_user_name, password=_password)
            if result[0] == None:
                return False
            else:
                return True
        except Exception as e:
            print(e)

class ItemInventory():
    def __init__(self):
        pass

    async def get_all_item(self):
        result = list(await Items.all().order_by('name_item'))
        return result

    async def get_ones_item(self, query):
        result = list(await Items.filter(name_item__icontains=query).order_by('name_item'))
        if len(result) != 0:
            return result
        else:
            result_1 = list(await Items.filter(lot__icontains=query).order_by('name_item'))
            if len(result_1) != 0:
                return result_1
            else:
                result_2 = list(await Items.filter(exp__icontains=query).order_by('name_item'))
                if len(result_2) != 0:
                    return result_2
                else:
                    return [None]

    async def add_item(self, _name_item, _quantity, _unit, _lot, _exp):
        try:
            result = await Items.create(name_item=_name_item, quantity=_quantity, unit=_unit, lot=_lot, exp=_exp)
            return True
        except Exception as e:
            print(e)
            return False

    async def update_item(self, _name, _quantity):
        try:
            print(f"recibo: {_name}")
            item = await Items.get(name_item=_name)
            item.quantity = _quantity
            await item.save()
        except Exception as e:
            print(f"{e}")

    async def update_info_item(self, _indx, _name, _quantity, _unit, _lot, _exp):
        try:
            print(f"recibo: {_name}")
            item = await Items.get(name_item=_indx)
            item.name_item = _name
            item.quantity = _quantity
            item.unit = _unit
            item.lot = _lot
            item.exp = _exp
            await item.save()
        except Exception as e:
            print(f"{e}")

    async def delete_item(self, _name):
        try:
            item = await Items.get(name_item=_name)
            await item.delete()
            await item.save()
        except Exception as e:
            print(f"{e}")

    async def verific_exist(self, _name):
        try:
            item = await Items.filter(name_item=_name)
            if item[0]: return False
        except Exception as e:
            if str(e) == "list index out of range":
                return True

class ExelInventory():
    def __init__(self):
        pass

    async def save_exel(self, id, name_doc1, name_doc2, name_doc3):
        result = await Exel.create(exel_id=id, name_docx_one=name_doc1, name_docx_two=name_doc2, name_docx_tre=name_doc3)
        print(result)

    async def get_name_exel(self, id):
        result = await Exel.filter(exel_id=id)
        return result

    async def update_info_exel(self, id, name_doc1, name_doc2, name_doc3):
        result = await Exel.filter(exel_id=id).first()
        result.name_docx_one = name_doc1
        result.name_docx_two = name_doc2
        result.name_docx_tre = name_doc3
        await result.save()
