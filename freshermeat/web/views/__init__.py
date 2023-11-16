from freshermeat.web.views import session_mgmt
from freshermeat.web.views import views
from freshermeat.web.views.admin import admin_bp
from freshermeat.web.views.api import v2
from freshermeat.web.views.organization import organization_bp
from freshermeat.web.views.organization import organizations_bp
from freshermeat.web.views.project import project_bp
from freshermeat.web.views.project import projects_bp
from freshermeat.web.views.stats import stats_bp
from freshermeat.web.views.submission import submission_bp
from freshermeat.web.views.submission import submissions_bp
from freshermeat.web.views.user import user_bp

__all__ = [
    "session_mgmt",
    "views",
    "admin_bp",
    "v2",
    "organization_bp",
    "organizations_bp",
    "project_bp",
    "projects_bp",
    "stats_bp",
    "submission_bp",
    "submissions_bp",
    "user_bp",
]
