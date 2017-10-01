from web.views.api import v1
from web.views import views, session_mgmt

__all__ = ['v1', 'views', 'session_mgmt']

import conf
from flask import request
from flask import g
