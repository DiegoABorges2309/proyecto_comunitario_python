from tortoise.models import Model
from tortoise import fields

class Users(Model):
    user_name = fields.CharField(max_length=20)
    password = fields.CharField(max_length=20)

class Items(Model):
    name_item = fields.CharField(max_length=50, null= False)
    quantity = fields.FloatField(null= False)
    unit = fields.CharField(max_length=10, null= False)
    lot = fields.CharField(max_length=25, null=True)
    exp = fields.DateField(null=True)

class Exel(Model):
    exel_id = fields.IntField(null= False)
    name_docx_one = fields.CharField(max_length=50, null= True)
    name_docx_two = fields.CharField(max_length=50, null=True)
    name_docx_tre = fields.CharField(max_length=50, null=True)