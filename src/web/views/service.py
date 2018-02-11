from flask import Blueprint, request, render_template, flash, url_for, \
                  redirect, abort

from web.models import Service

service_bp = Blueprint('service_bp', __name__,
                       url_prefix='/service')


@service_bp.route('/<service_name>', methods=['GET'])
def service(service_name=None):
    #service_id = request.args.get('name')
    service = Service.query.filter(Service.name == service_name).first()
    if service is None:
        abort(404)
    if not service:
        flash('Unknown service.', 'warning')
        return redirect(url_for(services_bp.list_services))
    return render_template('service.html', service=service)
