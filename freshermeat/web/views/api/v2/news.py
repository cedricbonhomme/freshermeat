#! /usr/bin/env python
from flask_restx import fields
from flask_restx import Namespace
from flask_restx import reqparse
from flask_restx import Resource

from freshermeat.models import News


news_ns = Namespace("news", description="News related operations")

# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("news_id", type=str, help="The id of the news.")
parser.add_argument(
    "project_id", type=str, help="Id of the project related to the news."
)
parser.add_argument("page", type=int, default=1, location="args")
parser.add_argument("per_page", type=int, location="args")


# Response marshalling
news = news_ns.model(
    "News",
    {
        "news_id": fields.String(
            description="The id of the news.",
        ),
        "news_url": fields.String(description="The URL of the news."),
        "title": fields.String(description="The title of the news."),
        "project_id": fields.String(description="The id of the project."),
        "published": fields.DateTime(description="Date of publication of the news."),
    },
)

news_list_fields = news_ns.model(
    "NewsList",
    {
        "metadata": fields.Raw(
            description="Metada related to the result (number of page, current page, total number of objects)."
        ),
        "data": fields.List(fields.Nested(news), description="List of news"),
    },
)


@news_ns.route("/")
class NewsList(Resource):
    """Create new news."""

    @news_ns.doc("list_news")
    @news_ns.expect(parser)
    @news_ns.marshal_list_with(news_list_fields, skip_none=True)
    def get(self):
        """List all news"""
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

        query = News.query
        for arg in args:
            if hasattr(News, arg):
                query = query.filter(getattr(News, arg) == args[arg])
            else:
                p_arg = arg.split("_")[1]
                query = query.filter(News.project.has(**{p_arg: args[arg]}))
        total = query.count()
        news = query.all()
        count = total

        result["data"] = news
        result["metadata"]["total"] = total
        result["metadata"]["count"] = count

        return result, 200
