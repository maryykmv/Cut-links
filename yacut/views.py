from flask import flash, redirect, render_template, url_for

from . import app

from .constants import (INDEX_TEMPLATE, INDEX_TEMPLATE,
                        REDIRECT_VIEW)
from .forms import URLMapForm
from .models import URLMap


MESSAGE_CREATE_URL = 'Ваша новая ссылка готова:'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    try:
        if form.validate_on_submit():
            if form.custom_id.data is None or form.custom_id.data == '':
                url_map = URLMap().data(short=None, url=form.original_link.data)
            else:
                url_map = URLMap().data(short=form.custom_id.data, url=form.original_link.data)
            flash(MESSAGE_CREATE_URL)
            form.custom_id.data = url_map['short_link']
            short_url = url_for(
                REDIRECT_VIEW, short=form.custom_id.data, _external=True)
    except Exception:
        pass
    return render_template(INDEX_TEMPLATE, **locals())


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap().get_short_url(short, True).original)
