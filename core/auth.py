'''
This service handles the authentication of the users. We need to 
configure it with json web tokens. I've found a good tutorial here: https://www.youtube.com/watch?v=e-_tsR0hVLQ
'''

from httplib2 import Credentials
import jwt # JSON web tokens 

from flask import jsonify, request
from core import app, db
from core.models import Urls
from core.shortener import Shortener, is_url

@app.route('/users/login', methods=['POST'])
def login():
    '''
    TODO: Implement the endpoint that handles the user login. Check the tutorial.
    '''
    pass
