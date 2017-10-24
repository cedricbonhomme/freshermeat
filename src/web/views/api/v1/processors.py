#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, flash
from flask_login import current_user
from flask_restless import ProcessingException

import lib.checks
from web.views.common import login_user_bundle
from web.models import User, Service, Request


def auth_func(*args, **kw):
    if request.authorization:
        user = User.query.filter(name == request.authorization.username).first()
        if not user:
            raise ProcessingException("Couldn't authenticate your user",
                                      code=401)
        if not user.check_password(request.authorization.password):
            raise ProcessingException("Couldn't authenticate your user",
                                      code=401)
        if not user.is_active:
            raise ProcessingException("User is desactivated", code=401)
        login_user_bundle(user)
    if not current_user.is_authenticated:
        raise ProcessingException(description='Not authenticated!', code=401)
    return True


def post_preprocessor(data=None, **kw):
    """Accepts a single argument, `data`, which is the dictionary of
    fields to set on the new instance of the model.
    """
    service_id = kw['result']['service_id']
    service = Service.query.filter(Service.id == service_id).first()
    checks = []
    for info in service.required_informations:
        if 'checks' in info:
            for check in info['checks']:
                check_function = getattr(lib.checks, check)
                parameter = kw['result']['required_informations'][info['name']]
                checks.append(check_function(parameter))
    if not all(checks):
        raise ProcessingException("Do not pass check", code=422)


def post_postprocessor(result=None, **kw):
    """Accepts a single argument, `result`, which is the dictionary
    representation of the created instance of the model.
    """
    pass
    # send the notification...
