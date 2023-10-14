from random import randrange, random
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
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
        if URLMap.query.filter_by(short=short).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        urlmap = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data
        )

        db.session.add(urlmap)
        db.session.commit()
        return redirect(url_for('index_view', id=urlmap.id))
    return render_template('index.html', form=form)