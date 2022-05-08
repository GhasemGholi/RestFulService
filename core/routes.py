'''
Specifies the routes to the endpoints of our API. 
Each method refers to an endpoint and method. Check the assignment's table 
and note that each table row represents a function. 

TODO: Check design and look if we want to merge some of our functions.
'''

from ast import Global
from glob import glob
from flask import Flask, redirect, url_for, jsonify, request, g
from sqlalchemy import false
from core import app_api, db_api
from core.models import Users
from core.shortener import Shortener, is_url
import sys

isLoggedIn = False
usersList = dict()
currentUser = ""

@app_api.before_first_request
def init_db():
    db_api.create_all()


@app_api.route('/', methods=['GET'])
def get_all():

    if not isLoggedIn:
        return make_response({'message': '403 forbidden, register first or login'}, 403)

    urls = usersList[currentUser].Urls.query.filter(usersList[currentUser].Urls.user == currentUser)
    response = [{"id": url.id, "original": url.original, "shortened": url.short, 'user':url.user} for url in urls]
    
    return make_response(response, 200)


@app_api.route('/', methods=['POST'])
def add_url():
    if not isLoggedIn:
        return make_response({'message': '403 forbidden, register first or login'}, 403)
        
    url = request.values.get("url")
    if not is_url(url):
        return make_response({'message': '400 Bad Request'}, 400)

    short_url = Shortener(url).shortenedUrl

    db_entry = usersList[currentUser].Urls(original=url, short=short_url, user=currentUser)
    db_api.session.add(db_entry)
    db_api.session.commit()

    return make_response({'id': db_entry.id}, 201)


@app_api.route('/', methods=['DELETE'])
def delete_all():
    if not isLoggedIn:
        return make_response({'message': '403 forbidden, register first or login'}, 403)
    
    usersList[currentUser].Urls.query.filter(usersList[currentUser].Urls.user == currentUser).delete()
    
    return make_response({'message': '404 Not Found'}, 404)
    

@app_api.route('/<id>', methods=['GET'])
def get_one(id):
    if not isLoggedIn:
        return make_response({'message': '403 forbidden, register first or login'}, 403)
    entry = usersList[currentUser].Urls.query.filter_by(id=id).first()

    print(entry.user, file=sys.stdout)
    if entry and entry.user == currentUser:
        return make_response({'id': int(entry.id), 'url': entry.original, 'shortened': entry.short, 'user':entry.user}, 302)
    else:
        return make_response({'message': '404 Not Found'}, 404)


@app_api.route('/<id>', methods=['DELETE'])
def delete_one(id):
    if not isLoggedIn:
        return make_response({'message': '403 forbidden, register first or login'}, 403)
    
    entry = usersList[currentUser].Urls.query.filter_by(id=id).first()
    if entry and entry.user == currentUser:
        db_api.session.delete(entry)
        db_api.session.commit()
        return make_response(None, 204)
    else: 
        return make_response({'message': '404 Not Found'}, 404)


@app_api.route('/<id>', methods=['PUT'])
def update_one(id):
    '''
    Handles a PUT request at endpoint /:id. Searches the id in the database 
    and replaces the url and short_url with the url from the query string.

    Parameters:
        id <int>: The id to replace
    Returns: 
        resp <obj>: JSON response. 
    '''
    
    if not isLoggedIn:
        return make_response({'message': '403 forbidden, register first or login'}, 403)
    
    entry = usersList[currentUser].Urls.query.filter_by(id=id).first()
    if not entry:
        return make_response({'message': '404 Not Found'}, 404)

    new_url = request.values.get('url')
    if not is_url(new_url):
        make_response({'message': '400 Bad Request'}, 400)

    short_url = Shortener(new_url).shortenedUrl
    entry.original = new_url
    entry.short = short_url
    return make_response({'message': '200 Success'}, 200)
    
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
    return make_response("LOGGED IN", 200)

@app_api.route('/currentuser', methods=['GET'])
def getCurrentUser():
    global currentUser
    return make_response(currentUser + " IS LOGGED IN", 200)

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
