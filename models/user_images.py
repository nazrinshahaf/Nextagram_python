from models.base_model import BaseModel
import peewee as pw
from models.user import User


class User_images(BaseModel):
    user = pw.ForeignKeyField(User, backref='user')
    image = pw.TextField(null = True)
    description = pw.TextField(null = True)