from flask import Blueprint, request, render_template, flash, url_for, redirect

from web.models import Project

service_bp = Blueprint('service_bp', __name__,
                       url_prefix='/service')
services_bp = Blueprint('services_bp', __name__,
                        url_prefix='/services')


@services_bp.route('/', methods=['GET'])
def list_services():
    return render_template('services.html')


@service_bp.route('/', methods=['GET'])
def service():
    project_name = request.args.get('name')
    if Project.query.filter(Project.name == project_name).count() == 0:
        flash('Unknown project.', 'warning')
        return redirect(url_for(services_bp.list_services))
    return render_template('service.html')
