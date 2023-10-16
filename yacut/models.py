from datetime import datetime
from http import HTTPStatus
import random
import re
import string

from flask import flash, url_for, render_template

from . import db
from .constants import (MAX_LENGTH_LONG_LINK, MAX_LENGTH_SHORT_ID,
                        LENGTH_SHORT_ID, INDEX_TEMPLATE,
                        REDIRECT_VIEW)
from .error_handlers import InvalidAPIUsage
from settings import CHARACTERS


CHAR_SET = r'[a-zA-Z0-9]'
MESSAGE_EXISTS_SHORT_URL = (
    'Предложенный вариант короткой ссылки уже существует.')
MESSAGE_CREATE_URL = 'Ваша новая ссылка готова:'
MESSAGE_NOT_EXISTS_BODY = 'Отсутствует тело запроса'
MESSAGE_REQUIRED_FIELD = '"url" является обязательным полем!'
MESSAGE_INVALID_VALUE = 'Указано недопустимое имя для короткой ссылки'


def check_symbols(short_id):
    return ''.join(re.findall(CHAR_SET, short_id)) == short_id


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_LONG_LINK), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT_ID), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_representation(self, value=False):
        if value:
            return dict(
                url=self.original,
                short_link=self.short
            )
        return dict(url=self.original)

    def from_dict(self, data):
        self.original = data['original']
        self.short = data['short']

    def get_unique_short_id(self):
        result = ''
        while len(result) != LENGTH_SHORT_ID:
            result += random.choice(CHARACTERS)
        if not self.is_short_url_exists(result):
            return result
        return self.get_unique_short_id()

    def is_short_url_exists(self, short_id, first_404=False):
        if first_404:
            return self.query.filter_by(short=short_id).first_or_404()
        return self.query.filter_by(short=short_id).first()

    def data_api(self, data):
        if ('custom_id' not in data or data['custom_id'] is None
                or data['custom_id'] == ''):
            short_id = self.get_unique_short_id()
        else:
            short_id = data['custom_id']
        if (len(short_id) > MAX_LENGTH_SHORT_ID
                or not check_symbols(short_id)):
            raise InvalidAPIUsage(MESSAGE_INVALID_VALUE, HTTPStatus.BAD_REQUEST)
        if self.is_short_url_exists(short_id) is not None:
            raise InvalidAPIUsage(
                MESSAGE_EXISTS_SHORT_URL, HTTPStatus.BAD_REQUEST)
        data['original'] = data['url']
        data['short'] = short_id
        self.from_dict(data)
        db.session.add(self)
        db.session.commit()
        self.short = url_for(REDIRECT_VIEW, short=self.short, _external=True)
        return self.to_representation(True)

    def data_form(self, form):
        short_id = form.custom_id.data
        if short_id is None or short_id == '':
            short_id = URLMap().get_unique_short_id()
        else:
            short_id = form.custom_id.data
        if (len(short_id) > MAX_LENGTH_SHORT_ID
                or not check_symbols(short_id)):
            flash(MESSAGE_INVALID_VALUE)
            short_id = URLMap().get_unique_short_id()
        if URLMap().is_short_url_exists(short_id):
            flash(MESSAGE_EXISTS_SHORT_URL)
            return render_template(INDEX_TEMPLATE, form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=short_id
        )
        form.custom_id.data = short_id
        db.session.add(url_map)
        db.session.commit()
        flash(MESSAGE_CREATE_URL)
        flash(url_for(
            REDIRECT_VIEW, short=form.custom_id.data, _external=True
        ), 'url')
