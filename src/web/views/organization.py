from flask import Blueprint, render_template

organization_bp = Blueprint('organization_bp', __name__,
                            url_prefix='/organization')
organizations_bp = Blueprint('organizations_bp', __name__,
                             url_prefix='/organizations')


@organizations_bp.route('/', methods=['GET'])
def list_organizations():
    return render_template('organizations.html')
