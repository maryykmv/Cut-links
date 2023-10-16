from datetime import datetime
import random
import re

from flask import flash, url_for, render_template

from . import db
from .constants import (MAX_LENGTH_LONG_LINK, MAX_LENGTH_SHORT_ID,
                        LENGTH_SHORT_ID, INDEX_TEMPLATE,
                        REDIRECT_VIEW, MESSAGE_INVALID_VALUE,
                        MESSAGE_EXISTS_SHORT_URL)
from settings import CHARACTERS


CHAR_SET = r'[a-zA-Z0-9]'
MESSAGE_CREATE_URL = 'Ваша новая ссылка готова:'
MESSAGE_NOT_EXISTS_BODY = 'Отсутствует тело запроса'
MESSAGE_REQUIRED_FIELD = '"url" является обязательным полем!'


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

    def check_symbols(self, short_id):
        return ''.join(re.findall(CHAR_SET, short_id)) == short_id

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

    def data_api(self, short_id, url):
        self.original = url
        self.short = short_id
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
                or not self.check_symbols(short_id)):
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
