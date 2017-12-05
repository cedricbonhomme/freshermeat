from web.views.api.v1.organization import blueprint_organization
from web.views.api.v1.project import blueprint_project
from web.views.api.v1.cve import blueprint_cve
from web.views.api.v1.request import blueprint_request

__all__ = [blueprint_organization, blueprint_project, blueprint_cve,
           blueprint_request]
