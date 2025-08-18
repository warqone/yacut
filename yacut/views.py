from http import HTTPStatus

from flask import flash, redirect, render_template, url_for

from settings import Config
from yacut import app, forms, models, error_handlers


@app.route('/', methods=['GET', 'POST'])
def index():
    form = forms.ShortLinkForm()
    short_url = None

    if form.validate_on_submit():
        original_link = form.original_link.data.strip()
        custom_id = (
            form.custom_id.data.strip() if form.custom_id.data else None
        )
        try:
            link = models.URLMap.create_short_url(original_link, custom_id)
            short_url = (
                f'{Config.DOMAIN}' + url_for(
                    'redirect_to_original', short_id=link.short
                )
            )
        except error_handlers.FormException as e:
            flash(e.message)

    return render_template('index.html', form=form, short_url=short_url)


@app.route('/<string:short_id>')
def redirect_to_original(short_id):
    url = models.URLMap.get_by_short_url(short_id)
    return redirect(url.original, HTTPStatus.FOUND)