#! /usr/bin/env python
#-*- coding: utf-8 -*-

import datetime
from flask import request, flash
from flask_login import current_user
from flask_restless import ProcessingException

#from web.views.common import login_user_bundle
from web.models import User

def auth_func(*args, **kw):
    if request.authorization:
        user = User.query.filter(name==request.authorization.username).first()
        if not user:
            raise ProcessingException("Couldn't authenticate your user",
                                        code=401)
        if not user.check_password(request.authorization.password):
            raise ProcessingException("Couldn't authenticate your user",
                                        code=401)
        if not user.is_active:
            raise ProcessingException("User is desactivated", code=401)
        #login_user_bundle(user)
    if not current_user.is_authenticated:
        raise ProcessingException(description='Not authenticated!', code=401)
    return True

def service_POST_preprocessor(data=None, **kw):
    """
    POST preprocessor for the creation of shelter.
    """
    data["user_id"] = current_user.id
    if current_user.is_admin:
        data["is_published"] = True
        #flash("Your shelter has been created." +
        #      " You can already edit it by clicking on the pen to the right of the screen.",
        #     'success')
    #else:
    #    flash("Thank you for entering your shelter in the shelter database. Your shelter " +
	#			  "will be visible in the database after a short review by the administrator. " +
	#		  "We kindly request you to add additional data about your shelter, such as " +
	#		  "technical documentation and drawings, and different attributes. You can edit your " +
	#		  "shelter when you log in to the website and go to 'your shelters'.", 'success');
