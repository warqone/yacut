from datetime import datetime
import random
import re
import string

from yacut import db, error_handlers
from yacut import constants as const


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(), nullable=False)
    short = db.Column(
        db.String(const.SHORT_LINK_LENGTH), nullable=False, unique=True,
        index=True
    )
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def get_unique_short_id():
        chars = string.ascii_letters + string.digits
        for _ in range(const.MAX_GENERATE_ITERATIONS):
            short_id = ''.join(
                random.choice(chars) for _ in range(
                    const.SHORT_LINK_GENERATE_LENGTH))
            if not URLMap.check_short_url(short_id):
                return short_id

    @staticmethod
    def create_short_url(
            original_url: str,
            short_url: str = None):
        if short_url:
            if URLMap.check_short_url(short_url):
                raise error_handlers.FormException(
                    'Предложенный вариант короткой ссылки уже существует.')
            elif not re.match(const.PATTERN_VALIDATION_SHORT_LINK, short_url):
                raise error_handlers.FormException(
                    'Указано недопустимое имя для короткой ссылки'
                )
        else:
            short_url = URLMap.get_unique_short_id()
        try:
            url_map = URLMap(original=original_url, short=short_url)
            db.session.add(url_map)
            db.session.commit()
            return url_map
        except Exception:
            db.session.rollback()
            raise error_handlers.FormException(
                'Не удалось создать короткую ссылку.'
            )

    @staticmethod
    def check_short_url(short_url: str):
        url = URLMap.query.filter_by(short=short_url).first()
        return url if url else None

    @staticmethod
    def get_by_short_url(short_url: str):
        url = URLMap.query.filter_by(short=short_url).first_or_404()
        return url