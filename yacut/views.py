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
    if not form.validate_on_submit():
        return render_template(INDEX_TEMPLATE, form=form)
    try:
        data = URLMap.create_data(short=form.custom_id.data, url=form.original_link.data)
        flash(MESSAGE_CREATE_URL)
        form.custom_id.data = data['short_link']
        short_url = url_for(
            REDIRECT_VIEW, short=form.custom_id.data, _external=True)
    except ValueError as error:
        flash(str(error))
    return render_template(INDEX_TEMPLATE, **locals())


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap.get(short, True).original)
