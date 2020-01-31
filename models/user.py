from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
from flask_login import UserMixin,current_user, login_user
import re
from playhouse.hybrid import hybrid_property
from config import S3_LOCATION


class User(BaseModel,UserMixin):
    name = pw.CharField(unique=False, null=True)
    username = pw.CharField(unique=True, null=True)
    password = pw.CharField(null=True)
    email = pw.CharField(unique=True, null=True)
    profile_image = pw.TextField(null = True, default = 'defualt.png')
    is_private = pw.BooleanField(default = False)
        
    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)
        
        if duplicate_username:
            self.errors.append('Username already taken')
        if duplicate_email:
            self.errors.append('Email already in use')

        # name validation
        elif len(self.name) < 5:
            self.errors.append('Please fill in a valid name')

        # username validattion
        elif len(self.username) < 3:
            self.errors.append('Username must be longer than 3 characters')
        elif re.search('[\s]',self.username):
            self.errors.append('Username must not contain whitspace')
        
        # email validation
        elif re.search('[@]',self.email) is None:
            self.errors.append('Please use a valid email')
        elif re.search('[.]',self.email) is None:
            self.errors.append('Please use a valid email')
        elif re.search('[\s]',self.email):
            self.errors.append('Email must not contain whitespace')
        
        # password validation
        # password length validation
        elif len(self.password) < 8:
            self.errors.append('Password length should more than 8')
        # password whitespace validation
        elif re.search('[\s]',self.password):
            self.errors.append("Password must not contain whitespace")
        # password number validation
        elif re.search('[0-9]',self.password) is None:
            self.errors.append("Password must contain number")
        # password capital validation
        elif re.search('[A-Z]',self.password) is None:
            self.errors.append("Password must contain at least one capital letter")
        # password special character validation
        elif re.search('[!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]',self.password) is None:
            self.errors.append("Password should contain at least one special character")
        # hashed password on save so its hashed in database
        else:
            self.password = generate_password_hash(self.password)

    @hybrid_property
    def image_path(self):
        return S3_LOCATION + self.profile_image