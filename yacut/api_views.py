from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .constants import REDIRECT_VIEW
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
        data = URLMap.data(short=data.get('custom_id'), url=data['url'])
    except ValueError as error:
        raise InvalidAPIUsage(str(error))
    data['short_link'] = url_for(
        REDIRECT_VIEW, short=data['short_link'], _external=True)
    return jsonify(data), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.get_short_url(short_id)
    if url_map is None:
        raise InvalidAPIUsage(MESSAGE_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify(url_map.to_representation()), HTTPStatus.OK
