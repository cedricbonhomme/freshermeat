#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from flask import request, flash
from flask_login import current_user
from flask_restless import ProcessingException

from web.views.common import login_user_bundle
from web.models import User


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


def post_postprocessor(result=None, **kw):
    """Accepts a single argument, `result`, which is the dictionary
    representation of the created instance of the model.
    """
    print(result)
    # send the notification...
