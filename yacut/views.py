from flask import flash, redirect, render_template, url_for

from . import app
from .constants import REDIRECT_VIEW, INDEX_TEMPLATE
from .forms import URLMapForm
from .models import URLMap


MESSAGE_SHORT_USE = 'Имя {} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template(INDEX_TEMPLATE, form=form)
    try:
        data = URLMap.create_data(
            short=form.custom_id.data,
            url=form.original_link.data
        )
    except ValueError as error:
        flash(str(error))
    else:
        form.custom_id.data = data.short
    return render_template(
        INDEX_TEMPLATE,
        form=form,
        short_url=url_for(
            REDIRECT_VIEW,
            short=form.custom_id.data,
            _external=True)
    )


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap.get(short, True).original)
