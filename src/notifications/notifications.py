#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from flask_mail import Message

from bootstrap import mail
# from web.models import User


def new_request_notification(request):
    """New request notification.
    """
    subject = "[{service}] New request".format(service=request.service.name)
    plaintext = render_template('emails/new_request.txt', request=request)

    msg = Message(subject,
                  recipients=[request.service.notification_email])
    msg.body = plaintext
    mail.send(msg)
