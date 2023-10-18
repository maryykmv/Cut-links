from datetime import datetime
from http import HTTPStatus
import random
import re

from flask import flash

from . import db
from .constants import (MAX_LONG_LENGTH, MAX_SHORT_LENGTH,
                        SHORT_LENGTH, VALID_CHARACTERS,
                        CHARACTERS, MESSAGE_INVALID_VALUE)
from .error_handlers import InvalidAPIUsage


MESSAGE_CREATE_URL = 'Ваша новая ссылка готова:'
MESSAGE_NOT_EXISTS_BODY = 'Отсутствует тело запроса'
MESSAGE_REQUIRED_FIELD = '"url" является обязательным полем!'
MESSAGE_EXISTS_SHORT = (
    'Предложенный вариант короткой ссылки уже существует.')


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LONG_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_representation(self, value=False):
        if value:
            return dict(
                url=self.original,
                short_link=self.short
            )
        return dict(url=self.original)

    @staticmethod
    def check_symbols(short):
        return set(re.sub(VALID_CHARACTERS, '', short))

    @staticmethod
    def get_unique_short():
        unique_short = ''.join(random.sample(CHARACTERS, SHORT_LENGTH))
        if URLMap.get_short_url(unique_short):
            URLMap.get_unique_short(unique_short)
        return unique_short

    @staticmethod
    def get_short_url(short, first_404=False):
        if first_404:
            return URLMap.query.filter_by(short=short).first_or_404()
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def data(short, url=None):
        if (short is None or short == ''):
            short = URLMap.get_unique_short()
        if (len(short) > MAX_SHORT_LENGTH or URLMap.check_symbols(short)):
            flash(MESSAGE_INVALID_VALUE), HTTPStatus.BAD_REQUEST
            raise ValueError(MESSAGE_INVALID_VALUE)
        if URLMap.get_short_url(short) is not None:
            flash(MESSAGE_EXISTS_SHORT)
            raise ValueError(
                MESSAGE_EXISTS_SHORT)
        url_map = URLMap(
            original=url,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map.to_representation(True)
