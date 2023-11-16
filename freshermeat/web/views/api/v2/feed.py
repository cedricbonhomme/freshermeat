from flask_restx import fields
from flask_restx import Namespace
from flask_restx import reqparse
from flask_restx import Resource

from freshermeat.bootstrap import db
from freshermeat.models import Feed
from freshermeat.web.views.api.v2.common import auth_func

feed_ns = Namespace("feed", description="Feed related operations.")

# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("feed_id", type=str, help="The id of the feed.")
parser.add_argument("page", type=int, default=1, location="args")
parser.add_argument("per_page", type=int, location="args")


# Response marshalling
feed = feed_ns.model(
    "Feed",
    {
        "feed_id": fields.String(
            description="The id of the feed.",
        ),
        "link": fields.String(description="The link of the feed."),
        "created_date": fields.DateTime(description="Created date."),
    },
)

feed_list_fields = feed_ns.model(
    "FeedsList",
    {
        "metadata": fields.Raw(
            description="Metada (number of page, current page, total number of items)."
        ),
        "data": fields.List(fields.Nested(feed), description="List of items."),
    },
)


@feed_ns.route("/")
class FeedsList(Resource):
    """Shows a list of all feeds."""

    @feed_ns.doc("list_feeds")
    @feed_ns.expect(parser)
    @feed_ns.marshal_list_with(feed_list_fields, skip_none=True)
    def get(self):
        """List all feeds."""
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

        query = Feed.query
        for arg in args:
            if hasattr(Feed, arg):
                query = query.filter(getattr(Feed, arg) == args[arg])
            else:
                p_arg = arg.split("_")[1]
                query = query.filter(Feed.project.has(**{p_arg: args[arg]}))
        total = query.count()
        feeds = query.all()
        count = total

        result["data"] = feeds
        result["metadata"]["total"] = total
        result["metadata"]["count"] = count

        return result, 200


@feed_ns.route("/<string:id>")
@feed_ns.response(404, "Feed not found")
@feed_ns.param("id", "The feed identifier")
class FeedItem(Resource):
    """Show a single feed item and lets you delete them."""

    @feed_ns.doc("get_feed")
    @feed_ns.marshal_with(feed)
    def get(self, id):
        """Fetch a given resource"""
        return Feed.query.filter(Feed.id == id).first(), 200

    @feed_ns.doc("delete_feed")
    @feed_ns.response(204, "Feed deleted")
    @feed_ns.doc(security="apikey")
    @auth_func
    def delete(self, id):
        """Delete a feed given its identifier."""
        Feed.query.filter(Feed.id == id).delete()
        db.session.commit()
        return "", 204
