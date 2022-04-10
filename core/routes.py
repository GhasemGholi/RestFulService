from flask import *
from core import app, db
from core.models import Urls
from core.shortener import Shortener


@app.before_first_request
def init_db():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    Set up the route to the index page. 
    '''
    if request.method == 'POST':
        url = request.form['URL_input']
        if is_url(url):
            pass
        db_entry = Urls(original=url, short=Shortener(url).shortenedUrl)
        db.session.add(db_entry)
        db.session.commit()
        # TODO: add to database
        return render_template('index.html')

    elif request.method == 'GET':
        return render_template('index.html')

    else: 
        return bad_request('400: Bad Request')
    

@app.route('/<name>', methods=['GET', 'PUT', 'DELETE'])
def index_param(name):
    

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