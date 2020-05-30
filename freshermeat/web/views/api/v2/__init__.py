from flask import Blueprint, request, render_template
from flask_restx import Api

from freshermeat.bootstrap import application


api_blueprint = Blueprint("api", __name__, url_prefix="/api/v2")


def setup_api(application):
    authorizations = {
        "apikey": {"type": "apiKey", "in": "header", "name": "X-API-KEY",}
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
        authorizations=authorizations
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

    from freshermeat.web.views.api.v2 import project

    api.add_namespace(project.project_ns, path="/api/v2/projects")

    return api


api = setup_api(application)
