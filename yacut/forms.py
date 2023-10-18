from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import MAX_LONG_LENGTH, MAX_SHORT_LENGTH, VALID_CHARACTERS

PLACEHOLDER_LONG_LINK = 'Длинная ссылка'
PLACEHOLDER_SHORT_LINK = 'Ваш вариант короткой ссылки'
REQUIRED_FIELD = 'Обязательное поле'
LABEL_BUTTON_CREATE = 'Создать'


class URLMapForm(FlaskForm):
    original_link = URLField(
        PLACEHOLDER_LONG_LINK,
        validators=[DataRequired(message=REQUIRED_FIELD),
                    Length(max=MAX_LONG_LENGTH)]
    )
    custom_id = StringField(
        PLACEHOLDER_SHORT_LINK,
        validators=[
            Length(max=MAX_SHORT_LENGTH),
            Regexp(VALID_CHARACTERS),
            Optional(strip_whitespace=False)
        ]
    )
    submit = SubmitField(LABEL_BUTTON_CREATE)
