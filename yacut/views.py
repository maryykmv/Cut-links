import re

from flask import redirect, render_template

from . import app
from .constants import (CHAR_SET, INDEX_TEMPLATE)
from .forms import URLMapForm
from .models import URLMap


def check_symbols(short_id):
    return re.fullmatch(CHAR_SET, short_id)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        URLMap().data_form(form)
    return render_template(INDEX_TEMPLATE, form=form)


@app.route('/<string:short>')
def redirect_view(short):
    url_map = URLMap().is_short_url_exists(short, True)
    return redirect(url_map.original)
