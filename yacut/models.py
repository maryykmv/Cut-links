from datetime import datetime
import random
import re

from flask import url_for

from . import db
from .constants import (MAX_LONG_LENGTH, MAX_SHORT_LENGTH,
                        SHORT_LENGTH, VALID_CHARACTERS,
                        CHARACTERS, REDIRECT_VIEW)


MESSAGE_EXISTS_SHORT = (
    'Предложенный вариант короткой ссылки уже существует.')
MESSAGE_SHORT_CREATE = 'Короткая ссылка не создана.'
MESSAGE_INVALID_VALUE = 'Указано недопустимое имя для короткой ссылки'
MESSAGE_LONG_INVALID = 'Размер длинной сылки превышает ограничение {}.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LONG_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_representation(self, value=False):
        if value:
            return dict(
                url=self.original,
                short_link=url_for(
                    REDIRECT_VIEW,
                    short=self.short,
                    _external=True)
            )
        return dict(url=self.original)

    @staticmethod
    def get_unique_short():
        for _ in range(len(VALID_CHARACTERS)):
            short = ''.join(random.choices(CHARACTERS, k=SHORT_LENGTH))
            if not URLMap.get(short):
                return short
        raise ValueError(MESSAGE_SHORT_CREATE)

    @staticmethod
    def get(short, first_404=False):
        if first_404:
            return URLMap.query.filter_by(short=short).first_or_404()
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def create_data(short, url=None, validate=False):
        if (short is None or short == ''):
            short = URLMap.get_unique_short()
        if validate:
            if len(url) > MAX_LONG_LENGTH:
                raise ValueError(MESSAGE_LONG_INVALID.format(MAX_LONG_LENGTH))
            if not re.fullmatch(VALID_CHARACTERS, short):
                raise ValueError(MESSAGE_INVALID_VALUE)
        if URLMap.get(short) is not None:
            raise ValueError(MESSAGE_EXISTS_SHORT)
        url_map = URLMap(
            original=url,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map
