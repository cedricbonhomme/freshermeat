from flask import Blueprint, render_template, jsonify
from datetime import datetime
from datetime import timedelta
from sqlalchemy import func

from bootstrap import db
from web.models import Project, License, Tag, Language, Organization, User

stats_bp = Blueprint('stats_bp', __name__, url_prefix='/stats')


@stats_bp.route('/', methods=['GET'])
def stats():
    """Returns a pages which displays global statistics about all projects."""
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
    result = db.session.query(func.lower(Tag.text),
                              func.count(func.lower(Tag.text))). \
                        group_by(func.lower(Tag.text)).all()
    return jsonify(dict(result))


@stats_bp.route('/organizations.json', methods=['GET'])
def organizations():
    """Returns a JSON with the different types of organizations (Non-profit, Governmental, etc.)."""
    result = db.session.query(Organization.organization_type,
                              func.count(Organization.organization_type)). \
                              group_by(Organization.organization_type).all()
    return jsonify(dict(result))


@stats_bp.route('/activity.json', methods=['GET'])
def activity():
    """Returns a JSON with the number of projects sorted by activity (by
    period of weeks)."""
    now = datetime.today()
    result = {}
    result['<= 12 weeks'] = db.session.query(Project). \
                filter(Project.last_updated >= now -
                                                timedelta(weeks=12)).count()
    result['12 weeks - 36 weeks'] = db.session.query(Project). \
                filter(Project.last_updated.between(
                                            now - timedelta(weeks=36),
                                            now - timedelta(weeks=12))).count()
    result['36 weeks - 1 year'] = db.session.query(Project). \
                filter(Project.last_updated.between(
                                            now - timedelta(weeks=52),
                                            now - timedelta(weeks=36))).count()
    result['1 year - 2 years'] = db.session.query(Project). \
                filter(Project.last_updated.between(
                                            now - timedelta(weeks=104),
                                            now - timedelta(weeks=52))).count()
    result['>= 2 years'] = db.session.query(Project). \
                filter(Project.last_updated <= now -
                                                timedelta(weeks=104)).count()
    return jsonify(result)


@stats_bp.route('/submitters.json', methods=['GET'])
def submitters():
    """Returns a JSON with the repartition of submitters."""
    result = db.session.query(User.login, func.count(User.id)). \
                              join(User.contributions).group_by(User.id).all()
    return jsonify(dict(result))
