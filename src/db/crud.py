import asyncio
from src.db.models import Users, Items

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

    async def add_item(self, _name_item, _quantity, _unit, _lot):
        try:
            result = await Items.create(name_item=_name_item, quantity=_quantity, unit=_unit, lot=_lot)
            print(result)
            if result:
                print("ok")
            else:
                print("no")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pass