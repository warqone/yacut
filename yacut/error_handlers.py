from http import HTTPStatus

from flask import render_template

from yacut import app


class InvalidAPIUsage(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message

        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


class FormException(BaseException):

    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    return render_template('404.html'), HTTPStatus.NOT_FOUND
