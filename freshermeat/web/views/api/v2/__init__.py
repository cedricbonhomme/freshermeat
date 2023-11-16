from flask import Blueprint, render_template
from flask_restx import Api

from freshermeat.bootstrap import application

api_blueprint = Blueprint("apiv2", __name__, url_prefix="/api/v2")


def setup_api(application):
    authorizations = {
        "apikey": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-KEY",
        }
    }

    api = Api(
        api_blueprint,
        title="Freshermeat - API v2",
        version="2.0",
        description="API v2 of Freshermeat.",
        license="GNU Affero General Public License version 3",
        license_url="https://www.gnu.org/licenses/agpl-3.0.html",
        doc="/",
        security="apikey",
        authorizations=authorizations,
    )

    @api.documentation
    def custom_ui():
        return render_template(
            "swagger-ui.html",
            title=api.title,
            specs_url="{}/api/v2/swagger.json".format(
                application.config["FRESHERMEAT_INSTANCE_URL"]
            ),
        )

    from freshermeat.web.views.api.v2 import (
        code,
        cve,
        feed,
        language,
        license,
        news,
        organization,
        project,
        release,
        user,
    )

    api.add_namespace(organization.organization_ns, path="/organization")
    api.add_namespace(project.project_ns, path="/projects")
    api.add_namespace(user.user_ns, path="/user")
    api.add_namespace(cve.cve_ns, path="/cve")
    api.add_namespace(release.release_ns, path="/release")
    api.add_namespace(news.news_ns, path="/news")
    api.add_namespace(license.license_ns, path="/license")
    api.add_namespace(language.language_ns, path="/language")
    api.add_namespace(code.code_ns, path="/code")
    api.add_namespace(feed.feed_ns, path="/feed")

    return api


api = setup_api(application)
