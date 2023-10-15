from http import HTTPStatus
from flask import jsonify, request, url_for

from . import app, db
from .constants import (MESSAGE_EXISTS_SHORT_URL, MESSAGE_NOT_EXISTS_BODY,
                        MESSAGE_REQUIRED_FIELD, MESSAGE_INVALID_VALUE,
                        MESSAGE_NOT_FOUND, MAX_LENGTH_SHORT_ID)
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import check_symbols, get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_short_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(MESSAGE_NOT_EXISTS_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(MESSAGE_REQUIRED_FIELD)
    if 'custom_id' not in data or data['custom_id'] is None or data['custom_id'] == '':
        short_id = get_unique_short_id()
    else:
        short_id = data['custom_id']
    if len(short_id) > MAX_LENGTH_SHORT_ID or not check_symbols(short_id):
        raise InvalidAPIUsage(MESSAGE_INVALID_VALUE, HTTPStatus.BAD_REQUEST)
    if URLMap.query.filter_by(short=short_id).first() is not None:
        raise InvalidAPIUsage(MESSAGE_EXISTS_SHORT_URL, HTTPStatus.BAD_REQUEST)
    urlmap = URLMap()
    data['original'] = data['url']
    data['short'] = short_id
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    urlmap.short = url_for('redirect_view', short=urlmap.short, _external=True)
    return jsonify(urlmap.to_dict(True)), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage(MESSAGE_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify(urlmap.to_dict()), HTTPStatus.OK