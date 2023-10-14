import re 
from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' not in data or data['custom_id'] is None or data['custom_id'] == '':
        short_id = get_unique_short_id()
    else:
        short_id = data['custom_id']
    if len(short_id) > 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)
    if URLMap.query.filter_by(short=short_id).first() is not None:
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.', 400)
    print(short_id)
    if short_id.isalnum():
        urlmap = URLMap()
        data['original'] = data['url']
        data['short'] = short_id
        urlmap.from_dict(data)
        db.session.add(urlmap)
        db.session.commit()
        urlmap.short = url_for('redirect_view', short=urlmap.short, _external=True)
        return jsonify(url=urlmap.original, short_link=urlmap.short), 201
    else:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', 400)


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify(url=urlmap.original), 200