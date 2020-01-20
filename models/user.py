from models.base_model import BaseModel
import peewee as pw

class User(BaseModel):
    name = pw.CharField(unique=False)
    username = pw.CharField(unique=True)
    password = pw.CharField()
    email = pw.CharField(unique=True)

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        # user.User.get_or_none(user.User.username == 'Boyeeeee')

        if duplicate_username:
            self.errors.append('Username already taken')
        if duplicate_email:
            self.errors.append('Email already in use')
        # if len(self.password) < 6:
        #     self.errors.append('Password should be more than 6 letters')
