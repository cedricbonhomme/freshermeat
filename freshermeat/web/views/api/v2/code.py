from flask_restx import fields
from flask_restx import Namespace
from flask_restx import reqparse
from flask_restx import Resource

from freshermeat.bootstrap import db
from freshermeat.models import Code
from freshermeat.web.views.api.v2.common import auth_func


code_ns = Namespace("code", description="Code related operations.")

# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("code_id", type=str, help="The id of the code (repository).")
parser.add_argument("page", type=int, default=1, location="args")
parser.add_argument("per_page", type=int, location="args")


# Response marshalling
code = code_ns.model(
    "Code",
    {
        "code_id": fields.String(
            description="The id of the code (repository).",
        ),
        "repository_url": fields.String(description="The URL of the repository."),
        "scm_type": fields.String(description="The type of the repository."),
        "last_updated": fields.DateTime(description="Last updated date."),
    },
)

code_list_fields = code_ns.model(
    "CodesList",
    {
        "metadata": fields.Raw(
            description="Metada (number of page, current page, total number of items)."
        ),
        "data": fields.List(fields.Nested(code), description="List of items."),
    },
)


@code_ns.route("/")
class CodesList(Resource):
    """Shows a list of all codes."""

    @code_ns.doc("list_codes")
    @code_ns.expect(parser)
    @code_ns.marshal_list_with(code_list_fields, skip_none=True)
    def get(self):
        """List all Codes."""
        args = parser.parse_args()
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

        query = Code.query
        for arg in args:
            if hasattr(Code, arg):
                query = query.filter(getattr(Code, arg) == args[arg])
            else:
                p_arg = arg.split("_")[1]
                query = query.filter(Code.project.has(**{p_arg: args[arg]}))
        total = query.count()
        codes = query.all()
        count = total

        result["data"] = codes
        result["metadata"]["total"] = total
        result["metadata"]["count"] = count

        return result, 200


@code_ns.route("/<string:id>")
@code_ns.response(404, "Code not found")
@code_ns.param("id", "The code identifier")
class CodeItem(Resource):
    """Show a single code item and lets you delete them."""

    @code_ns.doc("get_code")
    @code_ns.marshal_with(code)
    def get(self, id):
        """Fetch a given resource."""
        return Code.query.filter(Code.id == id).first(), 200

    @code_ns.doc("delete_code")
    @code_ns.response(204, "Code deleted")
    @code_ns.doc(security="apikey")
    @auth_func
    def delete(self, id):
        """Delete a code given its identifier."""
        Code.query.filter(Code.id == id).delete()
        db.session.commit()
        return "", 204
