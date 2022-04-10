from flask import *
from core import app, db
from core.models import Urls


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def index():
    '''
    Set up the route to the index page. 
    '''
    return render_template('index.html')
    

def is_url(url):
    '''
    TODO: Return boolean containing the validity of the URL.
    '''
    return url


def bad_request(msg):
    resp = jsonify({'message': msg})
    resp.status_code = 400
    return resp


def request_not_found(msg):
    resp = jsonify({'message': msg})
    resp.status_code = 404
    return resp


if __name__ == '__main__':
    app.run(port=5000, debug=True)