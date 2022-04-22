#! /usr/bin/env python
from flask_restx import fields
from flask_restx import Namespace
from flask_restx import reqparse
from flask_restx import Resource

from freshermeat.bootstrap import db
from freshermeat.models import Release
from freshermeat.web.views.api.v2.common import auth_func


release_ns = Namespace("release", description="Release related operations")

# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("release_id", type=str, help="The id of the release.")
parser.add_argument(
    "project_id", type=str, help="Id of the project related to the release."
)
parser.add_argument("page", type=int, default=1, location="args")
parser.add_argument("per_page", type=int, location="args")


# Response marshalling
release = release_ns.model(
    "Release",
    {
        "release_id": fields.String(
            description="The id of the release.",
        ),
        "version": fields.String(description="The version of the release."),
        "changes": fields.String(description="The changes related to the release."),
        "release_url": fields.String(description="The URL of the release."),
        "project_id": fields.String(description="The id of the project."),
        "published_at": fields.DateTime(
            description="Date of publication of the release."
        ),
    },
)

release_list_fields = release_ns.model(
    "ReleasesList",
    {
        "metadata": fields.Raw(
            description="Metada related to the result (number of page, current page, total number of objects)."
        ),
        "data": fields.List(fields.Nested(release), description="List of releases"),
    },
)


@release_ns.route("/")
class ReleasesList(Resource):
    """Create new releases."""

    @release_ns.doc("list_releases")
    @release_ns.expect(parser)
    @release_ns.marshal_list_with(release_list_fields, skip_none=True)
    def get(self):
        """List all releases"""
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

        query = Release.query
        for arg in args:
            if hasattr(Release, arg):
                query = query.filter(getattr(Release, arg) == args[arg])
            else:
                p_arg = arg.split("_")[1]
                query = query.filter(Release.project.has(**{p_arg: args[arg]}))
        total = query.count()
        releases = query.all()
        count = total

        result["data"] = releases
        result["metadata"]["total"] = total
        result["metadata"]["count"] = count

        return result, 200


@release_ns.route("/<string:id>")
@release_ns.response(404, "Release not found")
@release_ns.param("id", "The release identifier")
class ReleaseItem(Resource):
    """Show a single release item and lets you delete them"""

    @release_ns.doc("get_release")
    @release_ns.marshal_with(release)
    def get(self, id):
        """Fetch a given resource"""
        return Release.query.filter(Release.id == id).first(), 200

    @release_ns.doc("delete_release")
    @release_ns.response(204, "Release deleted")
    @release_ns.doc(security="apikey")
    @auth_func
    def delete(self, id):
        """Delete a release given its identifier"""
        Release.query.filter(Release.id == id).delete()
        db.session.commit()
        return "", 204
