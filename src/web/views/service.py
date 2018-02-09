from flask import Blueprint, request, render_template, flash, url_for, redirect

from web.models import Service

service_bp = Blueprint('service_bp', __name__,
                       url_prefix='/service')
services_bp = Blueprint('services_bp', __name__,
                        url_prefix='/services')


@services_bp.route('/', methods=['GET'])
def list_services():
    return render_template('services.html')


@service_bp.route('/', methods=['GET'])
def service():
    service_id = request.args.get('name')
    service = Service.query.filter(Service.id == service_id).first()
    if not service:
        flash('Unknown service.', 'warning')
        return redirect(url_for(services_bp.list_services))
    return render_template('service.html', service=service)
