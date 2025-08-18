from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

from yacut import constants as const


class ShortLinkForm(FlaskForm):
    original_link = StringField(
        'Введите оригинальную ссылку',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(
                min=const.MIN_LINK_LENGTH,
                max=const.MAX_LINK_LENGTH,
                message=f'Длина ссылки должна быть от '
                f'{const.MIN_LINK_LENGTH} до {const.MAX_LINK_LENGTH} символов.'
            )
        ]
    )
    custom_id = StringField(
        'Введите короткую ссылку',
        validators=[
            Length(
                max=const.SHORT_LINK_LENGTH,
                message=(
                    'Длина короткой ссылки должна быть не больше '
                    f'{const.SHORT_LINK_LENGTH} символов.'
                )
            ),
            Regexp(
                const.PATTERN_VALIDATION_SHORT_LINK,
                message='Недопустимые символы в короткой ссылке.'
            )
        ]
    )
    submit = SubmitField('Создать')
