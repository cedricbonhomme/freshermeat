#! /usr/bin/env python
from flask_restx import fields
from flask_restx import Namespace
from flask_restx import reqparse
from flask_restx import Resource

from freshermeat.models import Language


language_ns = Namespace("language", description="Language related operations")

# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("language_id", type=str, help="The id of the language.")
parser.add_argument("name", type=str, help="The name of the language.")
parser.add_argument("page", type=int, default=1, location="args")
parser.add_argument("per_page", type=int, location="args")


# Response marshalling
language = language_ns.model(
    "Language",
    {
        "id": fields.String(
            description="The id of the language.",
        ),
        "name": fields.String(description="The name of the language."),
        "created_at": fields.DateTime(description="Date of creation of the language."),
    },
)

language_list_fields = language_ns.model(
    "LanguagesList",
    {
        "metadata": fields.Raw(
            description="Metada related to the result (number of page, current page, total number of objects)."
        ),
        "data": fields.List(fields.Nested(language), description="List of languages"),
    },
)


@language_ns.route("/")
class LanguagesList(Resource):
    """Create new languages."""

    @language_ns.doc("list_languages")
    @language_ns.expect(parser)
    @language_ns.marshal_list_with(language_list_fields, skip_none=True)
    def get(self):
        """List all languages."""
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

        query = Language.query
        for arg in args:
            if hasattr(Language, arg):
                query = query.filter(getattr(Language, arg) == args[arg])
            else:
                p_arg = arg.split("_")[1]
                query = query.filter(Language.project.has(**{p_arg: args[arg]}))
        total = query.count()
        languages = query.all()
        count = total

        result["data"] = languages
        result["metadata"]["total"] = total
        result["metadata"]["count"] = count

        return result, 200
