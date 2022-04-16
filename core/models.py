'''
Specifies the database models for our API. this is where we perform 
our CRUD operations.
'''

from lib2to3.pgen2 import token
from sqlalchemy import true
from core import db
import jwt
from flask import Flask, jsonify, g
from core import app
import random 
import string

class Urls(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    original = db.Column("original", db.String())
    short = db.Column("shortened", db.String())

    def __init__(self, original, short) -> None:
        self.original = original
        self.short = short

class Users(db.Model):
    '''
    TODO: Implement a database model for the users. 
          Should contain id, username and hashed password at least. 
    '''
    key = db.Column("key", db.String())
    user = db.Column("user", db.String())
    password = db.Column("password", db.String())
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

    id = db.Column("id", db.Integer, primary_key=True)