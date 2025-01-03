from tortoise.models import Model
from tortoise import fields

class Users(Model):
    user_name = fields.CharField(max_length=20)
    password = fields.CharField(max_length=20)

