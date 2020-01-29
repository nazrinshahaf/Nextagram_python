from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.user_images import User_images
from config import S3_LOCATION
from playhouse.hybrid import hybrid_property
from flask_login import current_user

class Payment(BaseModel):

    user = pw.ForeignKeyField(User, backref='donations')
    image = pw.ForeignKeyField(User_images, backref='donations')
    amount = pw.IntegerField(null = False, default= 5)
    message = pw.TextField(null=True)
    
