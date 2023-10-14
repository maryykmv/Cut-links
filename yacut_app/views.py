import random
import string

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap

LENGTH_SHORT_ID = 6


def get_unique_short_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(LENGTH_SHORT_ID))


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        if short_id:
            if URLMap.query.filter_by(short=short_id).first():
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('index.html', form=form)
        else:
            short_id = get_unique_short_id()
        urlmap = URLMap(
            original=form.original_link.data,
            short=short_id
        )
        form.custom_id.data = short_id
        db.session.add(urlmap)
        db.session.commit()
        flash('Ваша новая ссылка готова:')
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    urlmap = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(urlmap.original)