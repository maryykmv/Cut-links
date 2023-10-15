import random
import re
import string

from flask import flash, redirect, render_template

from . import app, db
from .constants import (LENGTH_SHORT_ID, CHAR_SET, MESSAGE_INVALID_VALUE,
                        MESSAGE_EXISTS_SHORT_URL, INDEX_TEMPLATE,
                        MESSAGE_CREATE_URL, MAX_LENGTH_SHORT_ID)
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id():
    return ''.join(random.choice(string.ascii_letters + string.digits)
                   for _ in range(LENGTH_SHORT_ID))


def check_symbols(short_id):
    return re.fullmatch(CHAR_SET, short_id)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        if short_id is None or short_id == '':
            short_id = get_unique_short_id()
        else:
            short_id = form.custom_id.data
        if len(short_id) > MAX_LENGTH_SHORT_ID or not check_symbols(short_id):
            flash(MESSAGE_INVALID_VALUE)
            short_id = get_unique_short_id()
        if URLMap.query.filter_by(short=short_id).first():
            flash(MESSAGE_EXISTS_SHORT_URL)
            return render_template(INDEX_TEMPLATE, form=form)
        urlmap = URLMap(
            original=form.original_link.data,
            short=short_id
        )
        form.custom_id.data = short_id
        db.session.add(urlmap)
        db.session.commit()
        flash(MESSAGE_CREATE_URL)
    return render_template(INDEX_TEMPLATE, form=form)


@app.route('/<string:short>')
def redirect_view(short):
    urlmap = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(urlmap.original)