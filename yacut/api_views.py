from flask import request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from settings import Config


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return error.to_dict(), error.status_code


@app.route('/api/id/', methods=['POST'])
def create_short_id():
    try:
        data = request.get_json()
    except Exception:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' in data and len(data['custom_id']) == 0:
        data.pop('custom_id')
    link = URLMap.create_short_url(
        data.get('url'), data.get('custom_id', None)
    )
    if not isinstance(link, URLMap):
        raise InvalidAPIUsage(link)
    return (
        {'url': link.original,
         'short_link': f'{Config.DOMAIN}/{link.short}'}, 201
    )


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if not link:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return {'url': link.original}