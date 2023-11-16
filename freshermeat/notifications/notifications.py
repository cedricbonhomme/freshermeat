#! /usr/bin/env python
import urllib.parse

from bootstrap import instance_domain_name, mail
from flask import render_template, url_for
from flask_mail import Message

# from web.models import User


def new_request_notification(request):
    """New request notification."""
    subject = f"[{request.service.name}] New request"
    platform_url = urllib.parse.urljoin(
        instance_domain_name(), url_for("admin_bp.view_request", request_id=request.id)
    )
    plaintext = render_template(
        "emails/new_request.txt", request=request, platform_url=platform_url
    )
    msg = Message(subject, recipients=[request.service.notification_email])

    msg.body = plaintext
    mail.send(msg)
