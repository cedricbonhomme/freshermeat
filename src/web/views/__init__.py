from web.views.api import v1
from web.views import views, session_mgmt
from web.views.admin import admin_bp
from web.views.project import project_bp, projects_bp

__all__ = ['v1', 'views', 'session_mgmt', 'admin_bp', 'project_bp',
           'projects_bp']
