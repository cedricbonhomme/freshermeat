from freshermeat.web.views.api.v1.organization import blueprint_organization
from freshermeat.web.views.api.v1.user import blueprint_user
from freshermeat.web.views.api.v1.project import blueprint_project
from freshermeat.web.views.api.v1.code import blueprint_code
from freshermeat.web.views.api.v1.tag import blueprint_tag
from freshermeat.web.views.api.v1.release import blueprint_release
from freshermeat.web.views.api.v1.cve import blueprint_cve
from freshermeat.web.views.api.v1.license import blueprint_license
from freshermeat.web.views.api.v1.language import blueprint_language
from freshermeat.web.views.api.v1.news import blueprint_news
from freshermeat.web.views.api.v1.feed import blueprint_feed

__all__ = [blueprint_organization, blueprint_project, blueprint_cve,
           blueprint_release, blueprint_user,
           blueprint_code, blueprint_license,
           blueprint_language, blueprint_news, blueprint_feed]
