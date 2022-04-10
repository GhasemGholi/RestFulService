from flask import Flask, render_template, jsonify


app = Flask(__name__)


@app.get('/')
def index():
    return render_template('./index.html')


def is_url():
    '''
    TODO: Return boolean containing the validity of the URL.
    '''
    pass


def bad_request(msg):
    resp = jsonify({'message': msg})
    resp.status_code = 400
    return resp


def request_not_found():
    resp = jsonify({'message': msg})
    resp.status_code = 404
    return resp

if __name__ == '__main__':
    app.run(port=5000, debug=True)