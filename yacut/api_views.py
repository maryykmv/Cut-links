from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


MESSAGE_NOT_FOUND = 'Указанный id не найден'
MESSAGE_REQUIRED_FIELD = '"url" является обязательным полем!'
MESSAGE_NOT_EXISTS_BODY = 'Отсутствует тело запроса'


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(MESSAGE_NOT_EXISTS_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(MESSAGE_REQUIRED_FIELD)
    try:
        url_map = URLMap.create(
            short=data.get('custom_id'),
            url=data.get('url'),
            validate=True
        )
    except ValueError as error:
        raise InvalidAPIUsage(str(error))
    return jsonify(url_map.to_representation()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.get(short_id)
    if url_map is None:
        raise InvalidAPIUsage(MESSAGE_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
