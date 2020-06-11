#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restx import Namespace, Resource, fields, reqparse

from freshermeat.models import CVE


cve_ns = Namespace(
    "cve", description="CVE related operations"
)

# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("cve_id", type=str, help="The id of the CVE.")
parser.add_argument("summary", type=str, help="The summary of the CVE.")
parser.add_argument("project_id", type=str, help="Id of the project related to the CVE.")
parser.add_argument("page", type=int, default=1, location="args")
parser.add_argument("per_page", type=int, location="args")


# Response marshalling
cve = cve_ns.model(
    "CVE",
    {
        "cve_id": fields.String(description="The id of the CVE.",),
        "summary": fields.String(description="The summary of the CVE."),
        "published_at": fields.DateTime(description="Date of publication of the CVE."),
    },
)

cve_list_fields = cve_ns.model(
    "CVEsList",
    {
        "metadata": fields.Raw(
            description="Metada related to the result (number of page, current page, total number of objects)."
        ),
        "data": fields.List(fields.Nested(cve), description="List of CVEs"),
    },
)


@cve_ns.route("/")
class CVEsList(Resource):
    """Create new CVEs."""

    @cve_ns.doc("list_cves")
    @cve_ns.expect(parser)
    @cve_ns.marshal_list_with(cve_list_fields, skip_none=True)
    def get(self):
        """List all CVEs"""
        args = parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}

        page = args.pop("page", 1)
        per_page = args.pop("per_page", 10)

        result = {
            "data": [],
            "metadata": {"total": 0, "count": 0, "page": page, "per_page": per_page,},
        }

        try:
            query = CVE.query
            for arg in args:
                if hasattr(CVE, arg):
                    query = query.filter(getattr(CVE, arg) == args[arg])
            total = query.count()
            cves = query.all()
            count = total
        except:
            return result, 200
        finally:
            if not cves:
                return result, 200

        result["data"] = cves
        result["metadata"]["total"] = total
        result["metadata"]["count"] = count

        return result, 200
