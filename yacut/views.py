from flask import abort, flash, redirect, render_template, url_for

from settings import Config
from . import app
from .forms import ShortLinkForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ShortLinkForm()

    if form.validate_on_submit():
        original_link = form.original_link.data.strip()
        custom_id = (
            form.custom_id.data.strip() if form.custom_id.data else None
        )
        link = URLMap.create_short_url(original_link, custom_id)
        if not isinstance(link, URLMap):
            flash(link, 'error')
            return render_template('index.html', form=form)
        flash(f'Ваша новая ссылка готова: {Config.DOMAIN}/{link.short}')
        return redirect(url_for('index'), 200)

    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_to_original(short_id):
    link = URLMap.get_by_short_url(short_id)
    if not link:
        return abort(404)
    return redirect(link, 302)