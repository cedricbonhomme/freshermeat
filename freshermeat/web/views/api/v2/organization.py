from flask_restx import fields
from flask_restx import Namespace
from flask_restx import reqparse
from flask_restx import Resource

from freshermeat.models import Organization

organization_ns = Namespace(
    "organization", description="Organization related operations."
)

# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("id", type=int, help="Id of the organization.")
parser.add_argument("name", type=str, help="Name of the organization.")
parser.add_argument("description", type=str, help="Description of the organization.")
parser.add_argument("organization_type", type=str, help="Type of the organization.")
parser.add_argument(
    "short_description", type=str, help="Short descripton of the organization."
)
parser.add_argument("website", type=int, help="Website of the organization.")
parser.add_argument("cve_vendor", type=int, help="CVE vendor of the organization.")
parser.add_argument("page", type=int, default=1, location="args")
parser.add_argument("per_page", type=int, location="args")


# Response marshalling
organization = organization_ns.model(
    "Organization",
    {
        "id": fields.Integer(
            readonly=True, description="The organization unique identifier."
        ),
        "name": fields.String(
            description="Name of the organization.",
        ),
        "description": fields.String(
            description="The description of the organization."
        ),
        "organization_type": fields.String(description="The type of the organization."),
        "short_description": fields.String(
            description="The short descripton of the organization."
        ),
        "website": fields.String(description="The website of the organization."),
        "cve_vendor": fields.String(description="CVE vendor of the organization."),
        "last_updated": fields.DateTime(
            description="Last update time of the organization."
        ),
    },
)

organization_list_fields = organization_ns.model(
    "OrganizationsList",
    {
        "metadata": fields.Raw(
            description="Metada (number of page, current page, total number of items)."
        ),
        "data": fields.List(fields.Nested(organization), description="List of items."),
    },
)


@organization_ns.route("/")
class OrganizationsList(Resource):
    """Shows a list of all organizations."""

    @organization_ns.doc("list_organizations")
    @organization_ns.expect(parser)
    @organization_ns.marshal_list_with(organization_list_fields, skip_none=True)
    def get(self):
        """List all organizations."""
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

        query = Organization.query
        for arg in args:
            if hasattr(Organization, arg):
                query = query.filter(getattr(Organization, arg) == args[arg])
        total = query.count()
        organizations = query.all()
        count = total

        result["data"] = organizations
        result["metadata"]["total"] = total
        result["metadata"]["count"] = count

        return result, 200
