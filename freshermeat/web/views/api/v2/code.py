#! /usr/bin/env python
from flask_restx import fields
from flask_restx import Namespace
from flask_restx import reqparse
from flask_restx import Resource

from freshermeat.models import Code


code_ns = Namespace("code", description="Code related operations")

# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("code_id", type=str, help="The id of the Code.")
parser.add_argument("page", type=int, default=1, location="args")
parser.add_argument("per_page", type=int, location="args")


# Response marshalling
code = code_ns.model(
    "Code",
    {
        "code_id": fields.String(
            description="The id of the Code.",
        ),
        "repository_url": fields.String(description="The URL of the code."),
        "scm_type": fields.String(description="The summary of the code."),
        "last_updated": fields.DateTime(description="Last updated date."),
    },
)

code_list_fields = code_ns.model(
    "CodesList",
    {
        "metadata": fields.Raw(
            description="Metada related to the result (number of page, current page, total number of objects)."
        ),
        "data": fields.List(fields.Nested(code), description="List of Code"),
    },
)


@code_ns.route("/")
class CodesList(Resource):
    """Create new Codes."""

    @code_ns.doc("list_codes")
    @code_ns.expect(parser)
    @code_ns.marshal_list_with(code_list_fields, skip_none=True)
    def get(self):
        """List all Code"""
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
