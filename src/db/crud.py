from src.db.models import Users

class UserLogin():
    def __init__(self):
        pass

    async def add_user(self, _user_name: str, _password: str):
        try:
            await Users.create(user_name=_user_name, password=_password)
            return True
        except Exception as e:
            print(e)
            return False

    async def verific_user(self, _user_name: str, _password: str):
        try:
            result = await Users.filter(user_name = _user_name, password = _password)
            if result[0] == None:
                return False
            else:
                return True
        except Exception as e:
            print(e)
