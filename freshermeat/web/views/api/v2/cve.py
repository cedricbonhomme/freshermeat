#! /usr/bin/env python
from flask_restx import Namespace, Resource, fields, reqparse

from freshermeat.models import CVE

cve_ns = Namespace("cve", description="CVE related operations.")

# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("cve_id", type=str, help="The id of the CVE.")
parser.add_argument("summary", type=str, help="The summary of the CVE.")
parser.add_argument(
    "project_id", type=str, help="Id of the project related to the CVE."
)
parser.add_argument(
    "project_name", type=str, help="Name of the project related to the CVE."
)
parser.add_argument("page", type=int, default=1, location="args")
parser.add_argument("per_page", type=int, location="args")


# Response marshalling
cve = cve_ns.model(
    "CVE",
    {
        "cve_id": fields.String(
            description="The id of the CVE.",
        ),
        "cve_url": fields.String(description="The URL of the CVE."),
        "summary": fields.String(description="The summary of the CVE."),
        "published_at": fields.DateTime(description="Date of publication of the CVE."),
    },
)

cve_list_fields = cve_ns.model(
    "CVEsList",
    {
        "metadata": fields.Raw(
            description="Metada (number of page, current page, total number of items)."
        ),
        "data": fields.List(fields.Nested(cve), description="List of items."),
    },
)


@cve_ns.route("/")
class CVEsList(Resource):
    """Shows a list of all CVEs."""

    @cve_ns.doc("list_cves")
    @cve_ns.expect(parser)
    @cve_ns.marshal_list_with(cve_list_fields, skip_none=True)
    def get(self):
        """List all CVEs."""
        args = parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        page = args.pop("page", 1) - 1
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

        query = CVE.query
        for arg in args:
            if hasattr(CVE, arg):
                query = query.filter(getattr(CVE, arg) == args[arg])
            else:
                p_arg = arg.split("_")[1]
                query = query.filter(CVE.project.has(**{p_arg: args[arg]}))

        query = query.order_by(CVE.published_at.desc())
        total = query.count()
        query = query.limit(per_page)
        results = query.offset(page * per_page)
        count = query.count()

        result["data"] = results
        result["metadata"]["total"] = total
        result["metadata"]["count"] = count

        return result, 200
