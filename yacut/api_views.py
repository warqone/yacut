from http import HTTPStatus

from flask import request

from yacut import app, error_handlers, models
from settings import Config


@app.errorhandler(error_handlers.InvalidAPIUsage)
def invalid_api_usage(error):
    return error.to_dict(), error.status_code


@app.route('/api/id/', methods=['POST'])
def create_short_id():
    try:
        data = request.get_json()
    except Exception:
        raise error_handlers.InvalidAPIUsage('Отсутствует тело запроса')
    if not data:
        raise error_handlers.InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise error_handlers.InvalidAPIUsage(
            '\"url\" является обязательным полем!'
        )
    try:
        link = models.URLMap.create_short_url(
            data.get('url'), data.get('custom_id', None)
        )
    except error_handlers.FormException as e:
        raise error_handlers.InvalidAPIUsage(e.message)
    return (
        {'url': link.original,
         'short_link': f'{Config.DOMAIN}/{link.short}'}, HTTPStatus.CREATED
    )


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_url(short_id):
    link = models.URLMap.query.filter_by(short=short_id).first()
    if not link:
        raise error_handlers.InvalidAPIUsage(
            'Указанный id не найден', HTTPStatus.NOT_FOUND
        )
    return {'url': link.original}