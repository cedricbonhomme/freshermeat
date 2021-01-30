#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.parse
from flask import render_template, url_for
from flask_mail import Message

from bootstrap import mail, application, instance_domain_name

# from web.models import User


def new_request_notification(request):
    """New request notification."""
    subject = "[{service}] New request".format(service=request.service.name)
    platform_url = urllib.parse.urljoin(
        instance_domain_name(), url_for("admin_bp.view_request", request_id=request.id)
    )
    plaintext = render_template(
        "emails/new_request.txt", request=request, platform_url=platform_url
    )
    msg = Message(subject, recipients=[request.service.notification_email])

    msg.body = plaintext
    mail.send(msg)
