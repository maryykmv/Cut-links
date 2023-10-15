from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from .constants import MAX_LENGTH_LONG_LINK, MAX_LENGTH_SHORT_ID

PLACEHOLDER_LONG_LINK = 'Длинная ссылка'
PLACEHOLDER_SHORT_LINK = 'Ваш вариант короткой ссылки'
REQUIRED_FIELD = 'Обязательное поле'
LABEL_BUTTON_CREATE = 'Создать'


class URLMapForm(FlaskForm):
    original_link = URLField(
        PLACEHOLDER_LONG_LINK,
        validators=[DataRequired(message=REQUIRED_FIELD),
                    Length(max=MAX_LENGTH_LONG_LINK)]
    )
    custom_id = StringField(
        PLACEHOLDER_SHORT_LINK,
        validators=[Length(max=MAX_LENGTH_SHORT_ID), Optional()]
    )
    submit = SubmitField(LABEL_BUTTON_CREATE)
