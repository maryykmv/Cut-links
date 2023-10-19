from flask import flash, redirect, render_template, url_for

from . import app
from .constants import REDIRECT_VIEW, INDEX_TEMPLATE
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    short_url = None
    if not form.validate_on_submit():
        return render_template(INDEX_TEMPLATE, form=form)
    try:
        short_url = url_for(
            REDIRECT_VIEW,
            short=URLMap.create(
                short=form.custom_id.data,
                url=form.original_link.data
            ).short,
            _external=True
        )
    except ValueError as error:
        flash(str(error))
    return render_template(
        INDEX_TEMPLATE,
        form=form,
        short_url=short_url
    )


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap.get(short, True).original)
