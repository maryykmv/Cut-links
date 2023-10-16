from flask import flash, redirect, render_template

from . import app

from .constants import (INDEX_TEMPLATE, MAX_LENGTH_SHORT_ID,
                        INDEX_TEMPLATE, MESSAGE_INVALID_VALUE,
                        MESSAGE_EXISTS_SHORT_URL)
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        url = form.original_link.data
        if short_id is None or short_id == '':
            short_id = URLMap().get_unique_short_id()
        else:
            short_id = form.custom_id.data
        if (len(short_id) > MAX_LENGTH_SHORT_ID
                or not URLMap().check_symbols(short_id)):
            flash(MESSAGE_INVALID_VALUE)
            short_id = URLMap().get_unique_short_id()
        if URLMap().is_short_url_exists(short_id):
            flash(MESSAGE_EXISTS_SHORT_URL)
            return render_template(INDEX_TEMPLATE, form=form)
        form.custom_id.data = short_id
        URLMap().data(short_id, url)
    return render_template(INDEX_TEMPLATE, form=form)


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap().is_short_url_exists(short, True).original)
