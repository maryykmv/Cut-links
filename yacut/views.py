from flask import flash, redirect, render_template, url_for

from . import app

from .constants import (INDEX_TEMPLATE, INDEX_TEMPLATE,
                        MESSAGE_EXISTS_SHORT, REDIRECT_VIEW)
from .forms import URLMapForm
from .models import URLMap


MESSAGE_CREATE_URL = 'Ваша новая ссылка готова:'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        if form.custom_id.data is None or form.custom_id.data == '':
            short = URLMap().verification_data(short=None)
        else:
            short = form.custom_id.data
        if URLMap().get_short_url(short):
            flash(MESSAGE_EXISTS_SHORT)
            return render_template(INDEX_TEMPLATE, form=form)
        form.custom_id.data = short
        URLMap().data(short, form.original_link.data)
        flash(MESSAGE_CREATE_URL)
        short_url = url_for(
            REDIRECT_VIEW, short=form.custom_id.data, _external=True)
    return render_template(INDEX_TEMPLATE, **locals())


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap().get_short_url(short, True).original)
