from web.views.api import v1
from web.views import views, session_mgmt
from web.views.admin import admin_bp
from web.views.user import user_bp, users_bp
from web.views.project import project_bp, projects_bp
from web.views.organization import organization_bp, organizations_bp
from web.views.service import service_bp

__all__ = ['v1', 'views', 'session_mgmt', 'admin_bp',
           'user_bp', 'users_bp',
           'project_bp', 'projects_bp',
           'organization_bp', 'organizations_bp',
           'service_bp']
