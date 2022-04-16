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
from core import app, db
from core.models import Urls, Users
from core.shortener import Shortener, is_url

isLoggedIn = False

@app.before_first_request
def init_db():
    db.create_all()


@app.route('/', methods=['GET'])
def get_all():
    global isLoggedIn
    
    if not isLoggedIn:
        return make_response({'message': 'YOU NEED TO LOGIN FIRST OR REGISTER'}, 400)
    urls = Urls.query.all()
    return make_response([{"id": url.id, "original": url.original, "shortened": url.short} for url in urls], 200)


@app.route('/', methods=['POST'])
def add_url():
    global isLoggedIn
    
    if not isLoggedIn:
        return make_response({'message': 'YOU NEED TO LOGIN FIRST OR REGISTER'}, 400)
        
    url = request.values.get("url")
    if not is_url(url):
        return make_response({'message': '400 Bad Request'}, 400)

    short_url = Shortener(url).shortenedUrl
    db_entry = Urls(original=url, short=short_url)
    db.session.add(db_entry)
    db.session.commit()

    return make_response({'id': db_entry.id}, 201)


@app.route('/', methods=['DELETE'])
def delete_all():
    global isLoggedIn
    
    if not isLoggedIn:
        return make_response({'message': 'YOU NEED TO LOGIN FIRST OR REGISTER'}, 400)
    Urls.query.delete()
    return make_response({'message': '404 Not Found'}, 404)
    

@app.route('/<id>', methods=['GET'])
def get_one(id):
    global isLoggedIn
    
    if not isLoggedIn:
        return make_response({'message': 'YOU NEED TO LOGIN FIRST OR REGISTER'}, 400)
    entry = Urls.query.filter_by(id=id).first()
    if entry:
        return make_response({'id': int(entry.id), 'url': entry.original, 'shortened': entry.short}, 302)
    else:
        return make_response({'message': '404 Not Found'}, 404)


@app.route('/<id>', methods=['DELETE'])
def delete_one(id):
    global isLoggedIn
    
    if not isLoggedIn:
        return make_response({'message': 'YOU NEED TO LOGIN FIRST OR REGISTER'}, 400)
    
    entry = Urls.query.filter_by(id=id).first()
    print(entry)
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return make_response(None, 204)
    else: 
        return make_response({'message': '404 Not Found'}, 404)


@app.route('/<id>', methods=['PUT'])
def update_one(id):
    '''
    Handles a PUT request at endpoint /:id. Searches the id in the database 
    and replaces the url and short_url with the url from the query string.

    Parameters:
        id <int>: The id to replace
    Returns: 
        resp <obj>: JSON response. 
    '''
    
    global isLoggedIn
    
    if not isLoggedIn:
        return make_response({'message': 'YOU NEED TO LOGIN FIRST OR REGISTER'}, 400)
    
    entry = Urls.query.filter_by(id=id).first()
    if not entry:
        return make_response({'message': '404 Not Found'}, 404)

    new_url = request.values.get('url')
    if not is_url(new_url):
        make_response({'message': '400 Bad Request'}, 400)

    short_url = Shortener(new_url).shortenedUrl
    entry.original = new_url
    entry.short = short_url
    return make_response({'message': '200 Success'}, 200)
    
@app.route('/users', methods=['POST'])
def register():
    user = request.values.get("user")
    password = request.values.get("password")
    
    if not user or not password:
        return make_response({'message': 'NO USERNAME AND PASSWORD PROVIDED'}, 400)
    if Users.query.filter_by(user=user).first():
        return make_response({'message': 'USERNAME ALREADY EXISTS'}, 400)

    credentials = Users(user=user, password=password)
    db.session.add(credentials)
    db.session.commit()
    return make_response({"username": credentials.user}, 201)

@app.route('/users/login', methods=['POST'])
def login():
    global isLoggedIn
    user = request.values.get("user")
    password = request.values.get("password")
    token = ""
    providedUser = Users.query.filter_by(user=user).first()
    
    if providedUser is not None:
        token = providedUser.checkToken()
    else:
        return make_response({'message': 'REGISTER FIRST'}, 400)

    if not token:
        if not user or not password:
            return make_response({'message': 'NO USERNAME AND PASSWORD PROVIDED'}, 400)
        
        if not providedUser or not providedUser.checkPassword(password):
            return make_response({'message': 'WRONG USERNAME OR WRONG PASSWORD'}, 400)
    
    isLoggedIn = True
    return make_response("LOGGED IN", 201)

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
