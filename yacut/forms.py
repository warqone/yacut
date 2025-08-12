from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ShortLinkForm(FlaskForm):
    original_link = StringField(
        'Введите оригинальную ссылку',
        validators=[
            DataRequired(message='Обязательное поле'),
        ]
    )
    custom_id = StringField(
        'Введите короткую ссылку',
        validators=[
            Length(
                max=16,
                message='Длина короткой ссылки должна быть не больше 16')
        ]
    )
    submit = SubmitField('Создать')