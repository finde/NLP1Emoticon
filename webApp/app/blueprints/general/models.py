# import datetime
#
# from app.extensions import db
#
#
# class User(db.Document):
#     username = db.StringField(required=True, unique=True)
#     email = db.EmailField(required=True, unique=True)
#     firstname = db.StringField(required=True)
#     lastname = db.StringField(required=True)
#     password = db.StringField(required=True)
#     joined = db.DateTimeField(default=datetime.datetime.now)
