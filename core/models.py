'''
Specifies the database models for our API. this is where we perform 
our CRUD operations.
'''

from lib2to3.pgen2 import token
from sqlalchemy import true
from core import db_api, db_users
import jwt
from flask import Flask, jsonify, g
from core import app_api, app_users
import random 
import string

class Urls(db_api.Model):
    id = db_api.Column("id", db_api.Integer, primary_key=True)
    original = db_api.Column("original", db_api.String())
    short = db_api.Column("shortened", db_api.String())

    def __init__(self, original, short) -> None:
        self.original = original
        self.short = short

class Users(db_users.Model):
    '''
    TODO: Implement a database model for the users. 
          Should contain id, username and hashed password at least. 
    '''
    id = db_users.Column("id", db_users.Integer, primary_key=True)
    key = db_users.Column("key", db_users.String())
    user = db_users.Column("user", db_users.String())
    password = db_users.Column("password", db_users.String())
    token = ""
    
    def __init__(self, user, password) -> None:
        self.user = user
        self.password = password
        self.key = self.tokenize()
        
    
    def checkToken(self):
        check = jwt.decode(self.key, "secret", algorithms=["HS256"])
        if check is not self.key:
            return False
        return True
    
    def checkPassword(self, password):
        if self.password is password:
            return True
        return False
                  
    def tokenize(self):
        token = jwt.encode({self.user : self.password}, "secret", algorithm="HS256")
        return token