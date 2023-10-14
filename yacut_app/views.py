from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id():
    pass


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        text = form.text.data
        if URLMap.query.filter_by(text=text).first():
            flash('Такое мнение уже было оставлено ранее!')
            return render_template('index.html', form=form)
        urlmap = URLMap(
            original=form.original_link.data,
            short=form.custom_id.data
        )
        db.session.add(urlmap)
        db.session.commit()
        return redirect(url_for('index_view', id=urlmap.id))
    return render_template('index.html', form=form)