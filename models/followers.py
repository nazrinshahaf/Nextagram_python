from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property
from flask_login import current_user


class Followers(BaseModel):
    follower = pw.ForeignKeyField(User, backref="following")
    followed = pw.ForeignKeyField(User, backref="followers")
