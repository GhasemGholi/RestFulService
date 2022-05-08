from ast import Global
from glob import glob
from flask import Flask, redirect, url_for, jsonify, request, g
from sqlalchemy import false
from admin import app_api, db_api
from admin.models import Users
import requests

isLoggedIn = False
usersList = dict()
currentUser = None

@app_api.before_first_request
def init_db():
    db_api.create_all()

@app_api.route('/', methods=['GET'])
def get_all():
    # urls = Urls.query.all()
    return make_response("YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", 200)

@app_api.route('/users', methods=['POST'])
def register():
    user = request.values.get("user")
    password = request.values.get("password")
    
    if not user or not password:
        return make_response({'message': '400 error, no user name or password provided'}, 400)
    if Users.query.filter_by(user=user).first():
        return make_response({'message': '403 forbidden, username already exists'}, 403)

    credentials = Users(user=user, password=password)
    db_api.session.add(credentials)
    db_api.session.commit()
    usersList[credentials.user] = credentials
    
    return make_response({"username": credentials.user}, 200)

@app_api.route('/users/login', methods=['POST'])
def login():
    global isLoggedIn
    global currentUser
    user = request.values.get("user")
    password = request.values.get("password")
    token = ""
    providedUser = Users.query.filter_by(user=user).first()
    
    if providedUser is not None:
        token = providedUser.checkToken()
    else:
        return make_response({'message': '400 forbidden, register first'}, 403)

    if not user or not password:
        return make_response({'message': '400 error, no username or password provided'}, 400)
    
    if not providedUser or not providedUser.checkPassword(password):
        return make_response({'message': '403 forbidden, wrong username or password'}, 403)
    
    currentUser = user
    isLoggedIn = True
    
    r = requests.get('http://127.0.0.1:5000/newlogin/'+user) 
    
    return make_response("LOGGED IN", 200)


@app_api.route('/currentuser', methods=['GET'])
def getCurrentUser():
    global currentUser
    if currentUser == None:
        return make_response({'message': '403 forbidden, login first'}, 403)
    return make_response(currentUser, 200)

def make_response(data, status_code):
    '''
    Make an HTTP response. 

    Parameters:
        data <dict>: the message to sent
        status_code <int>: HTTP status code to send.
    Returns:
        resp <obj>: JSON response. 

    '''
    resp = jsonify(data)
    resp.status_code = status_code
    return resp
