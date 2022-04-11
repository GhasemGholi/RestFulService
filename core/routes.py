from flask import jsonify, request
from core import app, db
from core.models import Urls
from core.shortener import Shortener, is_url


@app.before_first_request
def init_db():
    db.create_all()


@app.route('/', methods=['GET'])
def get_all():
    urls = Urls.query.all()
    return make_response([{"id": url.id, "original": url.original, "shortened": url.short} for url in urls], 200)


@app.route('/', methods=['POST'])
def add_url():
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
    Urls.query.delete()
    return make_response({'message': '404 Not Found'}, 404)
    

@app.route('/<id>', methods=['GET'])
def get_one(id):
    entry = Urls.query.filter_by(id=id).first()
    if entry:
        return make_response({'id': int(entry.id), 'url': entry.original, 'shortened': entry.short}, 301)
    else:
        return make_response({'message': '404 Not Found'}, 404)


@app.route('/<id>', methods=['DELETE'])
def delete_one(id):
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
    entry = Urls.query.filter_by(id=id).first()
    if not entry:
        return make_response({'message': '404 Not Found'}, 404)

    new_url = request.values.get('url')
    if not is_url(new_url):
        make_response({'message': '400 Bad Request'}, 400)

    if not is_url(new_url):
        return make_response({'message': '400 Bad Request'}, 400)

    short_url = Shortener(new_url).shortenedUrl
    entry.original = new_url
    entry.short = short_url
    return make_response({'message': '200 Success'}, 200)
        

def make_response(data, status_code):
    resp = jsonify(data)
    resp.status_code = status_code
    return resp