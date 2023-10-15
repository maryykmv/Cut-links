from http import HTTPStatus
from flask import jsonify, request

from . import app
from .constants import MESSAGE_NOT_FOUND
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    data = request.get_json()
    return jsonify(URLMap().data_api(data)), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap().is_short_url_exists(short_id)
    if url_map is None:
        raise InvalidAPIUsage(MESSAGE_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify(url_map.to_dict()), HTTPStatus.OK
