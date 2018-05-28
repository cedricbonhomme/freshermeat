from flask import Blueprint, render_template, jsonify

from sqlalchemy import func
from bootstrap import db
from web.models import Project, License, Tag, Language, Organization

stats_bp = Blueprint('stats_bp', __name__, url_prefix='/stats')


@stats_bp.route('/', methods=['GET'])
def stats():
    head_titles = ['Statistics']
    return render_template('stats.html', head_titles=head_titles)


@stats_bp.route('/licenses.json', methods=['GET'])
def licenses():
    """Returns a JSON with the repartition of licenses per projects."""
    result = db.session.query(License.name, func.count(License.id)). \
                              join(License.projects).group_by(License.id).all()
    return jsonify(dict(result))


@stats_bp.route('/languages.json', methods=['GET'])
def languages():
    """Returns a JSON with the repartition of languages per projects."""
    result = db.session.query(Language.name, func.count(Language.id)). \
                              join(Language.projects). \
                              group_by(Language.id).all()
    return jsonify(dict(result))


@stats_bp.route('/tags.json', methods=['GET'])
def tags():
    """Returns a JSON with the repartition of tags per projects."""
    result = db.session.query(Tag.text, func.count(Tag.text)). \
                              group_by(Tag.text).all()
    return jsonify(dict(result))


@stats_bp.route('/organizations.json', methods=['GET'])
def organizations():
    """Returns a JSON with the different types of organizations (Non-profit, Governmental, etc.)."""
    result = db.session.query(Organization.organization_type,
                              func.count(Organization.organization_type)). \
                              group_by(Organization.organization_type).all()
    return jsonify(dict(result))
