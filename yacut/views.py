from flask import redirect, render_template

from . import app
from .constants import INDEX_TEMPLATE
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        URLMap().data_form(form)
    return render_template(INDEX_TEMPLATE, form=form)


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap().is_short_url_exists(short, True).original)
