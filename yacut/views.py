from http import HTTPStatus

from flask import flash, redirect, render_template

from settings import Config
from yacut import app, forms, models, error_handlers


@app.route('/', methods=['GET', 'POST'])
def index():
    form = forms.ShortLinkForm()

    if form.validate_on_submit():
        original_link = form.original_link.data.strip()
        custom_id = (
            form.custom_id.data.strip() if form.custom_id.data else None
        )
        try:
            link = models.URLMap.create_short_url(original_link, custom_id)
        except error_handlers.FormException as e:
            flash(e.message, 'error')
            return render_template('index.html', form=form)
        flash('Ваша новая ссылка готова:')
        flash(f'{Config.DOMAIN}/{link.short}', 'link')

    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_to_original(short_id):
    url = models.URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url.original, HTTPStatus.FOUND)