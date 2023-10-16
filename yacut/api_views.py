from http import HTTPStatus
from flask import jsonify, request

from . import app

from .constants import (MAX_LENGTH_SHORT_ID, MESSAGE_INVALID_VALUE,
                        MESSAGE_EXISTS_SHORT_URL)
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
    if ('custom_id' not in data or data['custom_id'] is None
            or data['custom_id'] == ''):
        short_id = URLMap().get_unique_short_id()
    else:
        short_id = data['custom_id']
    if (len(short_id) > MAX_LENGTH_SHORT_ID
            or not URLMap().check_symbols(short_id)):
        raise InvalidAPIUsage(MESSAGE_INVALID_VALUE, HTTPStatus.BAD_REQUEST)
    if URLMap().is_short_url_exists(short_id) is not None:
        raise InvalidAPIUsage(
            MESSAGE_EXISTS_SHORT_URL, HTTPStatus.BAD_REQUEST)
    return jsonify(URLMap().data(short_id, data['url'])), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap().is_short_url_exists(short_id)
    if url_map is None:
        raise InvalidAPIUsage(MESSAGE_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify(url_map.to_representation()), HTTPStatus.OK
