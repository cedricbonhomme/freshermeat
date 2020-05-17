from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_restx import Api, Resource, fields, reqparse

from freshermeat.bootstrap import db, application
from freshermeat.models import Project
from freshermeat.web.views.api.v2.common import auth_func


blueprint = Blueprint("api", __name__, url_prefix="/api/v2/projects")
api = Api(
    blueprint,
    title="Freshermeat - API v2",
    version="2.0",
    description="API v2 of Freshermeat.",
    doc="/swagger/",
    # decorators = [auth_func]
    # All API metadatas
)


@api.documentation
def custom_ui():
    return render_template(
        "swagger-ui.html",
        title=api.title,
        specs_url="{}/api/v2/projects/swagger.json".format(
            application.config["FRESHERMEAT_INSTANCE_URL"]
        ),
    )


# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("name", type=str, help="Name of the project.")
parser.add_argument("description", type=str, help="Description of the project.")
parser.add_argument(
    "short_description", type=str, help="Short descripton of the project."
)
parser.add_argument("website", type=int, help="Website of the project.")
parser.add_argument("page", type=int, default=1, location="args")
parser.add_argument("per_page", type=int, location="args")


# Response marshalling
project = api.model(
    "Project",
    {
        "id": fields.Integer(
            readonly=True, description="The project unique identifier"
        ),
        "name": fields.String(description="Name of the project.",),
        "description": fields.String(description="The description of the project."),
        "short_description": fields.String(
            description="The short descripton of the project."
        ),
        "website": fields.String(description="The website of the project."),
        "organization": fields.String(
            attribute=lambda x: x.organization.name if x.organization else None,
            description="The organization related to this project.",
        ),
        "last_updated": fields.DateTime(description="Last update time of the project."),
    },
)

project_list_fields = api.model(
    "ProjectsList",
    {
        "metadata": fields.Raw(
            description="Metada related to the result (number of page, current page, total number of objects)."
        ),
        "data": fields.List(fields.Nested(project), description="List of projects"),
    },
)


@api.route("/")
class ProjectsList(Resource):
    """Shows a list of all projects, and lets you POST to add new projects"""

    @api.doc("list_projects")
    @api.expect(parser)
    @api.marshal_list_with(project_list_fields, skip_none=True)
    def get(self):
        """List all projects"""
        args = parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}

        page = args.pop("page", 1)
        per_page = args.pop("per_page", 10)

        result = {
            "data": [],
            "metadata": {"total": 0, "count": 0, "page": page, "per_page": per_page,},
        }

        try:
            query = Project.query
            for arg in args:
                if hasattr(Project, arg):
                    query = query.filter(getattr(Project, arg) == args[arg])
            total = query.count()
            projects = query.all()
            count = total
        except:
            return result, 200
        finally:
            if not projects:
                return result, 200

        result["data"] = projects
        result["metadata"]["total"] = total
        result["metadata"]["count"] = count

        return result, 200

    @api.doc("create_project")
    @api.expect(project)
    @api.marshal_with(project, code=201)
    @auth_func
    def post(self):
        """Create a new project"""
        new_project = Project(**api.payload)
        db.session.add(new_project)
        db.session.commit()
        return new_project, 201


@api.route("/<string:id>")
@api.response(404, "Project not found")
@api.param("id", "The project identifier")
class projectItem(Resource):
    """Show a single project item and lets you delete them"""

    @api.doc("get_project")
    @api.marshal_with(project)
    def get(self, id):
        """Fetch a given resource"""
        return Project.query.filter(Project.id == id).first(), 200

    @api.doc("delete_project")
    @api.response(204, "Project deleted")
    @auth_func
    def delete(self, id):
        """Delete a project given its identifier"""
        # DAO.delete(id)
        return "", 204

    @api.expect(project)
    @api.marshal_with(project)
    @auth_func
    def put(self, id):
        """Update a project given its identifier"""
        # return DAO.update(id, api.payload)
        pass
