'''
Specifies the database models for our API. this is where we perform 
our CRUD operations.
'''

from lib2to3.pgen2 import token
from sqlalchemy import true
from core import db_api
import jwt
from flask import Flask, jsonify, g
from core import app_api
import hashlib

class Users(db_api.Model):
    '''
    TODO: Implement a database model for the users. 
          Should contain id, username and hashed password at least. 
    '''
    id = db_api.Column("id", db_api.Integer(), primary_key=True)
    key = db_api.Column("key", db_api.LargeBinary())
    user = db_api.Column("user", db_api.String())
    password = db_api.Column("password", db_api.String())
    token = ""
        
    class Urls(db_api.Model):
        id = db_api.Column("id", db_api.Integer, primary_key=True)
        original = db_api.Column("original", db_api.String())
        short = db_api.Column("shortened", db_api.String())
        user = db_api.Column("user", db_api.String())
        
        def __init__(self, original, short, user) -> None:
            self.original = original
            self.short = short
            self.user = user

    def __init__(self, user, password) -> None:
        self.user = user
        self.password = self.hashPassword(password)
        self.key = self.tokenize()
        # self.id = self.createID()    
        
    def hashPassword(self, password):
        shaHashedPwd = hashlib.sha256(password.encode()).hexdigest()
        return shaHashedPwd

    def checkToken(self):
        check = jwt.decode(self.key, "secret", algorithms=["HS256"])
        if check != {self.user : self.password}:
            return False
        return True

    def checkPassword(self, password):
        if self.password == self.hashPassword(password):
            return True
        return False
                  
    def tokenize(self):
        token = jwt.encode({self.user : self.password}, "secret", algorithm="HS256")
        return token
    
    def getUser(self):
        return self.user
    
    # def createID(self):
    #     return secrets.token_bytes(nbytes=8)
    
    def getID(self):
        return self.id