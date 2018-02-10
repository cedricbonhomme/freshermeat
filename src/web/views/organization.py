from flask import Blueprint, render_template, abort

from web.models import Organization

organization_bp = Blueprint('organization_bp', __name__,
                            url_prefix='/organization')
organizations_bp = Blueprint('organizations_bp', __name__,
                             url_prefix='/organizations')


@organizations_bp.route('/', methods=['GET'])
def list_organizations():
    return render_template('organizations.html')


@organization_bp.route('/<string:organization_name>', methods=['GET'])
def get(organization_name=None):
    organization = Organization.query.filter(Organization.name == organization_name).first()
    if organization is None:
        abort(404)
    return render_template('organization.html', organization=organization)
