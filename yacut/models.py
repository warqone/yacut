from datetime import datetime
import random
import re
import string

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(255), nullable=False)
    short = db.Column(
        db.String(16), nullable=False, unique=True, index=True
    )
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def get_unique_short_id():
        chars = string.ascii_letters + string.digits
        while True:
            short_id = ''.join(random.choice(chars) for _ in range(6))
            if not URLMap.query.filter_by(short=short_id).first():
                return short_id

    @staticmethod
    def create_short_url(
            original_url: str,
            short_url: str = None):
        if short_url is not None:
            if URLMap.query.filter_by(short=short_url).first():
                return 'Предложенный вариант короткой ссылки уже существует.'
            elif not re.match(r'^[a-zA-Z0-9]+$', short_url) \
                    or len(short_url) > 16:
                return 'Указано недопустимое имя для короткой ссылки'
        else:
            short_url = URLMap.get_unique_short_id()
        try:
            url_map = URLMap(original=original_url, short=short_url)
            db.session.add(url_map)
            db.session.commit()
            return url_map
        except Exception:
            db.session.rollback()
            return 'Не удалось создать короткую ссылку.'

    @staticmethod
    def get_by_short_url(short_url: str):
        url = URLMap.query.filter_by(short=short_url).first()
        if url:
            return url.original
        return None