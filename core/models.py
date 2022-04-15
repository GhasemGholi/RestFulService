'''
Specifies the database models for our API. this is where we perform 
our CRUD operations.
'''

from core import db

class Urls(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    original = db.Column("original", db.String())
    short = db.Column("short", db.String())

    def __init__(self, original, short) -> None:
        self.original = original
        self.short = short

class Users(db.Model):
    '''
    TODO: Implement a database model for the users. 
          Should contain id, username and hashed password at least. 
    '''
    id = db.Column("id", db.Integer, primary_key=True)
