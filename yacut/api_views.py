from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import (MAX_LENGTH_SHORT, MESSAGE_INVALID_VALUE,
                        MESSAGE_EXISTS_SHORT)
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
    if ('custom_id' not in data or data['custom_id'] is None or data['custom_id'] == ''):
        short = URLMap().verification_data(short=None)
    else:
        short = URLMap().verification_data(data['custom_id'])
    return jsonify(URLMap().data(short, data['url'])), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap().get_short_url(short_id)
    if url_map is None:
        raise InvalidAPIUsage(MESSAGE_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify(url_map.to_representation()), HTTPStatus.OK
