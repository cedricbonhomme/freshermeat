from flask import Blueprint, render_template, jsonify

from sqlalchemy import func
from bootstrap import db
from web.models import Project, License

stats_bp = Blueprint('stats_bp', __name__, url_prefix='/stats')


@stats_bp.route('/', methods=['GET'])
def stats():
    return render_template('stats.html')


@stats_bp.route('/licenses.json', methods=['GET'])
def licenses(service_name=None):
    result = db.session.query(License.name, func.count(License.id)). \
                              join(License.projects).group_by(License.id).all()
    return jsonify(dict(result))
