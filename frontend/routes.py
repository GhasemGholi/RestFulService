from calendar import c
from glob import glob
from sys import stdout
from flask import jsonify, request
from frontend import app_api, db_api
from frontend.models import MessageBuilder
from frontend.shortener import Shortener, is_url
import requests
import re
from sqlalchemy.inspection import inspect

currentUser = ""
isLoggedIn = False
usersList = dict()
currentUserId = 0

@app_api.before_first_request
def init_db():
    db_api.create_all()
    checkLoggedIn()


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
    
    usersList[currentUser].Urls.query.filter_by(user=currentUser).delete()
    
    return make_response({'message': '404 Not Found'}, 404)
    

@app_api.route('/<id>', methods=['GET'])
def get_one(id):
    if not isLoggedIn:
        return make_response({'message': '403 forbidden, register first or login'}, 403)
    
    entry = usersList[currentUser][id]

    if entry and entry.user == currentUser:
        return make_response({'id': int(entry.id), 'url': entry.original, 'shortened': entry.short, 'user':entry.user}, 302)
    else:
        return make_response({'message': '404 Not Found'}, 404)


@app_api.route('/<id>', methods=['DELETE'])
def delete_one(id):
    if not isLoggedIn:
        return make_response({'message': '403 forbidden, register first or login'}, 403)
    
    entry = usersList[currentUser].query.filter_by(id=id).first()
    if entry and entry.user == currentUser:
        db_api.session.delete(entry)
        db_api.session.commit()
        return make_response(None, 204)
    else: 
        return make_response({'message': '404 Not Found'}, 404)


@app_api.route('/<id>', methods=['PUT'])
def update_one(id):
    if not isLoggedIn:
        return make_response({'message': '403 forbidden, register first or login'}, 403)
    
    entry = usersList[currentUser].query.filter_by(id=id).first()
    if not entry:
        return make_response({'message': '404 Not Found'}, 404)

    new_url = request.values.get('url')
    if not is_url(new_url):
        make_response({'message': '400 Bad Request'}, 400)

    short_url = Shortener(new_url).shortenedUrl
    entry.original = new_url
    entry.short = short_url
    return make_response({'message': '200 Success'}, 200)

@app_api.route('/isLoggedIn', methods=['POST'])       
def checkLoggedIn():
    r = requests.get('http://127.0.0.1:5001/currentuser') 

    if r.status_code == 403:
        return make_response({'message': '403 Login first'}, 403)
    
    global currentUser, isLoggedIn
    currentUser = re.sub('[^A-Za-z0-9]+', '', r.text)
    isLoggedIn = True
    
    usersList[currentUser] = MessageBuilder()
    
@app_api.route('/newlogin/<login>', methods=['GET'])       
def newLogInDetected(login):    
    global currentUser, isLoggedIn
    currentUser = login
    isLoggedIn = True
    
    usersList[currentUser] = MessageBuilder()
    
    return make_response(login + ' is logged in', 200)

@app_api.route('/currentuser', methods=['GET'])
def getCurrentUser():
    global currentUser
    if currentUser == None:
        return make_response({'message': '403 forbidden, login first'}, 403)
    return make_response(currentUser, 200)

def make_response(data, status_code):
    resp = jsonify(data)
    resp.status_code = status_code
    return resp