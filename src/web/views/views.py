import logging
from flask import render_template, flash, url_for, redirect, current_app, \
                    request

from web.models import Service


logger = logging.getLogger(__name__)


@current_app.errorhandler(401)
def authentication_required(error):
    flash('Authentication required.', 'info')
    return redirect(url_for('login'))


@current_app.errorhandler(403)
def authentication_failed(error):
    flash('Forbidden.', 'danger')
    return redirect(url_for('login'))


@current_app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@current_app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html'), 500


@current_app.errorhandler(AssertionError)
def handle_sqlalchemy_assertion_error(error):
    return error.args[0], 400


@current_app.route('/', methods=['GET'])
def services():
    return render_template('services.html')


@current_app.route('/service', methods=['GET'])
def service():
    service_name = request.args.get('name')
    if Service.query.filter(Service.name == service_name).count() == 0:
        flash('Unknown service.', 'warning')
        return redirect(url_for('services'))
    return render_template('service.html')
