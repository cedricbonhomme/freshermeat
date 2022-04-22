from flask_restx import fields
from flask_restx import Namespace
from flask_restx import reqparse
from flask_restx import Resource

from freshermeat.models import User


user_ns = Namespace("user", description="User related operations.")

# Argument Parsing
parser = reqparse.RequestParser()
parser.add_argument("user_id", type=str, help="The id of the user.")
parser.add_argument("login", type=str, help="The login of the user.")
parser.add_argument("page", type=int, default=1, location="args")
parser.add_argument("per_page", type=int, location="args")


# Response marshalling
user = user_ns.model(
    "User",
    {
        "user_id": fields.String(
            description="The id of the user.",
        ),
        "login": fields.String(description="The login of the user."),
    },
)

user_list_fields = user_ns.model(
    "UsersList",
    {
        "metadata": fields.Raw(
            description="Metada (number of page, current page, total number of items)."
        ),
        "data": fields.List(fields.Nested(user), description="List of items."),
    },
)


@user_ns.route("/")
class UsersList(Resource):
    """Shows a list of all users."""

    @user_ns.doc("list_users")
    @user_ns.expect(parser)
    @user_ns.marshal_list_with(user_list_fields, skip_none=True)
    def get(self):
        """List all users."""
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

        query = User.query
        for arg in args:
            if hasattr(User, arg):
                query = query.filter(getattr(User, arg) == args[arg])
            else:
                p_arg = arg.split("_")[1]
                query = query.filter(User.project.has(**{p_arg: args[arg]}))
        total = query.count()
        users = query.all()
        count = total

        result["data"] = users
        result["metadata"]["total"] = total
        result["metadata"]["count"] = count

        return result, 200
