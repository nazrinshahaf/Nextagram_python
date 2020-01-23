from models.base_model import BaseModel
import peewee as pw
from models.user import User
from config import S3_LOCATION
from playhouse.hybrid import hybrid_property
from flask_login import current_user

class User_images(BaseModel):
    user = pw.ForeignKeyField(User, backref='images')
    image = pw.TextField(null = True)
    description = pw.TextField(null = True)

    @hybrid_property
    def image_path(self):
        return S3_LOCATION + self.image