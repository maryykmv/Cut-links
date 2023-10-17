from flask import flash, redirect, render_template, url_for

from . import app

from .constants import (INDEX_TEMPLATE, MAX_LENGTH_SHORT,
                        INDEX_TEMPLATE, MESSAGE_INVALID_VALUE,
                        MESSAGE_EXISTS_SHORT, REDIRECT_VIEW)
from .forms import URLMapForm
from .models import URLMap


MESSAGE_CREATE_URL = 'Ваша новая ссылка готова:'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        url = form.original_link.data
        if short is None or short == '':
            short = URLMap().get_unique_short()
        else:
            short = form.custom_id.data
        if (len(short) > MAX_LENGTH_SHORT
                or URLMap().check_symbols(short)):
            flash(MESSAGE_INVALID_VALUE)
            short = URLMap().get_unique_short()
        if URLMap().get_short_url(short):
            flash(MESSAGE_EXISTS_SHORT)
            return render_template(INDEX_TEMPLATE, form=form)
        form.custom_id.data = short
        flash(MESSAGE_CREATE_URL)
        flash(url_for(
            REDIRECT_VIEW, short=short, _external=True
        ), 'url')
        URLMap().data(short, url)
    return render_template(INDEX_TEMPLATE, form=form)


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap().get_short_url(short, True).original)
