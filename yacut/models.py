from datetime import datetime
from http import HTTPStatus
import random
import re

from flask import flash, url_for
from . import db

from .constants import (MAX_LENGTH_LONG_LINK, MAX_LENGTH_SHORT,
                        LENGTH_SHORT, REDIRECT_VIEW, CHAR_SET,
                        CHARACTERS, MESSAGE_INVALID_VALUE,
                        MESSAGE_EXISTS_SHORT)
from .error_handlers import InvalidAPIUsage


MESSAGE_CREATE_URL = 'Ваша новая ссылка готова:'
MESSAGE_NOT_EXISTS_BODY = 'Отсутствует тело запроса'
MESSAGE_REQUIRED_FIELD = '"url" является обязательным полем!'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_LONG_LINK), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_representation(self, value=False):
        self.short = url_for(REDIRECT_VIEW, short=self.short, _external=True)
        if value:
            return dict(
                url=self.original,
                short_link=self.short
            )
        return dict(url=self.original)

    @staticmethod
    def check_symbols(short):
        return set(re.sub(CHAR_SET, '', short))

    @staticmethod
    def get_unique_short():
        unique_short = ''.join(random.sample(CHARACTERS, LENGTH_SHORT))
        if URLMap().get_short_url(unique_short):
            URLMap().get_unique_short(unique_short)
        return unique_short

    @staticmethod
    def get_short_url(short, first_404=False):
        if first_404:
            return URLMap().query.filter_by(short=short).first_or_404()
        return URLMap().query.filter_by(short=short).first()

    @staticmethod
    def verification_data(short):
        if (short is None or short == ''):
            return URLMap().get_unique_short()
        if (len(short) > MAX_LENGTH_SHORT or URLMap().check_symbols(short)):
            flash(MESSAGE_INVALID_VALUE), HTTPStatus.BAD_REQUEST
            raise InvalidAPIUsage(MESSAGE_INVALID_VALUE, HTTPStatus.BAD_REQUEST)
        if URLMap().get_short_url(short) is not None:
            flash(MESSAGE_EXISTS_SHORT)
            raise InvalidAPIUsage(
                MESSAGE_EXISTS_SHORT, HTTPStatus.BAD_REQUEST)
        return short

    def data(self, short, url):
        self.original = url
        self.short = short
        db.session.add(self)
        db.session.commit()
        return self.to_representation(True)
