from flask_restx import Namespace, Resource, fields, reqparse

from freshermeat.models import License

license_ns = Namespace("license", description="License related operations")

# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("license_id", type=str, help="The id of the license.")
parser.add_argument("name", type=str, help="The id of the license.")
parser.add_argument("page", type=int, default=1, location="args")
parser.add_argument("per_page", type=int, location="args")


# Response marshalling
license = license_ns.model(
    "License",
    {
        "id": fields.String(
            description="The id of the license.",
        ),
        "name": fields.String(description="The name of the license."),
        "license_id": fields.String(description="The id of the license."),
        "created_at": fields.DateTime(description="Date of creation of the license."),
    },
)

license_list_fields = license_ns.model(
    "LicensesList",
    {
        "metadata": fields.Raw(
            description="Metada (number of page, current page, total number of items)."
        ),
        "data": fields.List(fields.Nested(license), description="List of items."),
    },
)


@license_ns.route("/")
class LicensesList(Resource):
    """Shows a list of all licences."""

    @license_ns.doc("list_license")
    @license_ns.expect(parser)
    @license_ns.marshal_list_with(license_list_fields, skip_none=True)
    def get(self):
        """List all licenses."""
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

        query = License.query
        for arg in args:
            if hasattr(License, arg):
                query = query.filter(getattr(License, arg) == args[arg])
            else:
                p_arg = arg.split("_")[1]
                query = query.filter(License.project.has(**{p_arg: args[arg]}))
        total = query.count()
        licenses = query.all()
        count = total

        result["data"] = licenses
        result["metadata"]["total"] = total
        result["metadata"]["count"] = count

        return result, 200
