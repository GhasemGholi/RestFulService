from flask import *
from core import app, db
from core.models import Urls
from core.shortener import Shortener


@app.before_first_request
def init_db():
    db.create_all()

@app.route('/', methods=['GET', 'POST', 'DELETE'])
def index():
    '''
    Set up the route to the index page. 
    '''
    if request.method == 'POST':
        url = request.form['URL_input']
        shortened = Shortener(url)
        if not shortened.is_url(url):
            flash('Please enter a valid URL.')
            return redirect(url_for('index',  urls=Urls.query.all()))

        db_entry = Urls(original=url, short=shortened.shortenedUrl)
        db.session.add(db_entry)
        db.session.commit()
    elif request.method == 'DELETE':
        Urls.__table__.drop()

    return render_template('index.html', urls=Urls.query.all())
    

@app.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def index_param(id):
    link = Urls.query.filter_by(id=id).first()
    if not link:
        flash('Please enter a valid URL.')
        return redirect(url_for('index',  urls=Urls.query.all()))
    
    if request.method == 'GET':
        return redirect(link.original)
    elif request.method == 'DELETE':
        link.delete()
        return render_template('index.html', urls=Urls.query.all())

def bad_request(msg):
    resp = jsonify({'message': msg})
    resp.status_code = 400
    return resp


def request_not_found(msg):
    resp = jsonify({'message': msg})
    resp.status_code = 404
    return resp