from flask_login import current_user
from flask_restx import fields
from flask_restx import Namespace
from flask_restx import reqparse
from flask_restx import Resource

from freshermeat.bootstrap import db
from freshermeat.models import Project
from freshermeat.web.views.api.v2.common import auth_func


project_ns = Namespace("projects", description="project related operations")


# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("name", type=str, help="Name of the project.")
parser.add_argument("description", type=str, help="Description of the project.")
parser.add_argument(
    "short_description", type=str, help="Short descripton of the project."
)
parser.add_argument("tags", type=str, help="Tags of the project.")
parser.add_argument("license", type=str, help="License of the project.")
parser.add_argument("language", type=str, help="Language of the project.")
parser.add_argument("website", type=int, help="Website of the project.")
parser.add_argument("organization", type=str, help="Organization of the project.")
parser.add_argument("page", type=int, default=1, location="args")
parser.add_argument("per_page", type=int, location="args")


# Response marshalling
project = project_ns.model(
    "Project",
    {
        "id": fields.Integer(
            readonly=True, description="The project unique identifier"
        ),
        "name": fields.String(
            description="Name of the project.",
        ),
        "description": fields.String(description="The description of the project."),
        "short_description": fields.String(
            description="The short descripton of the project."
        ),
        "tag_objs": fields.List(fields.String(description="List of tags.")),
        "licenses": fields.List(fields.String(description="List of licenses.")),
        "languages": fields.List(fields.String(description="List of languages.")),
        "website": fields.String(description="The website of the project."),
        "organization": fields.String(
            attribute=lambda x: x.organization.name if x.organization else None,
            description="The organization related to this project.",
        ),
        "last_updated": fields.DateTime(description="Last update time of the project."),
    },
)

project_list_fields = project_ns.model(
    "ProjectsList",
    {
        "metadata": fields.Raw(
            description="Metada related to the result (number of page, current page, total number of objects)."
        ),
        "data": fields.List(fields.Nested(project), description="List of projects"),
    },
)


@project_ns.route("/")
class ProjectsList(Resource):
    """Shows a list of all projects, and lets you POST to add new projects"""

    @project_ns.doc("list_projects")
    @project_ns.expect(parser)
    @project_ns.marshal_list_with(project_list_fields, skip_none=True)
    def get(self):
        """List all projects"""
        args = parser.parse_args()
        project_organization = args.pop("organization", None)
        project_license = args.pop("license", None)
        project_language = args.pop("language", None)
        args = {k: v for k, v in args.items() if v is not None}

        page = args.pop("page", 1)
        per_page = args.pop("per_page", 10)

        result = {
            "data": [],
            "metadata": {
                "total": 0,
                "count": 0,
                "page": page,
                "per_page": per_page,
            },
        }

        query = Project.query
        for arg in args:
            if hasattr(Project, arg):
                query = query.filter(getattr(Project, arg) == args[arg])
        # Filter on other attributes
        if project_organization is not None:
            query = query.filter(Project.organization.has(name=project_organization))
        if project_license is not None:
            query = query.filter(Project.licenses.any(name=project_license))
        if project_language is not None:
            query = query.filter(Project.languages.any(name=project_language))

        total = query.count()
        projects = query.all()
        count = total

        result["data"] = projects
        result["metadata"]["total"] = total
        result["metadata"]["count"] = count

        return result, 200

    @project_ns.doc("create_project")
    @project_ns.expect(project)
    @project_ns.marshal_with(project, code=201)
    @project_ns.doc(security="apikey")
    @auth_func
    def post(self):
        """Create a new project"""
        project_ns.payload["submitter_id"] = current_user.id
        new_project = Project(**project_ns.payload)
        db.session.add(new_project)
        db.session.commit()
        return new_project, 201


@project_ns.route("/<string:id>")
@project_ns.response(404, "Project not found")
@project_ns.param("id", "The project identifier")
class projectItem(Resource):
    """Show a single project item and lets you delete them"""

    @project_ns.doc("get_project")
    @project_ns.marshal_with(project)
    def get(self, id):
        """Fetch a given resource"""
        return Project.query.filter(Project.id == id).first(), 200

    @project_ns.doc("delete_project")
    @project_ns.response(204, "Project deleted")
    @project_ns.doc(security="apikey")
    @auth_func
    def delete(self, id):
        """Delete a project given its identifier"""
        # DAO.delete(id)
        return "", 204

    @project_ns.expect(project)
    @project_ns.marshal_with(project)
    @project_ns.doc(security="apikey")
    @auth_func
    def put(self, id):
        """Update a project given its identifier"""
        # return DAO.update(id, project_ns.payload)
        pass
