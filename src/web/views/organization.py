from flask import Blueprint, render_template, request, abort
from werkzeug.contrib.atom import AtomFeed

from bootstrap import db
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


@organization_bp.route('/<string:organization_name>/releases.atom', methods=['GET'])
def recent_releases(organization_name=None):
    """Generates a feed for the releases."""
    organization = Organization.query. \
                        filter(Organization.name==organization_name).first()
    if organization is None:
        abort(404)
    feed = AtomFeed('Recent releases for {}'.format(organization.name),
                     feed_url=request.url, url=request.url_root)
    for project in organization.projects:
        for release in project.releases:
            feed.add(release.version, release.changes,
                     id=release.id,
                     url=release.release_url,
                     updated=release.published_at)
    return feed.get_response()
