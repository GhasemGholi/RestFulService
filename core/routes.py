from flask import *
from core import app, db
from core.models import Urls

app = Flask(__name__)
app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQL_ALCHEMY_DATABSE_URI'] = 'sqlite:///urls.db'


@app.before_first_request
def init_tables():
    '''
    Initialize the table containing the urls.
    '''
    db.create_all()


@app.get('/')
def index():
    '''
    Set up the route to the index page. 
    '''
    # Handle incoming POST request
    if request.method == 'POST':
        url = request.form['url']

        if not is_url(url):
            flash('Please enter a valid URL')
            return redirect(url_for('index'))

        return render_template('./index.html')

    elif request.method == 'GET':
        return render_template('./index.html')
    
    else: 
        return bad_request('This request method is invalid.')


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