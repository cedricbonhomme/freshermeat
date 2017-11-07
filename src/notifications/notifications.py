#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template

from bootstrap import application
from notifications import emails
# from web.models import User


# def information_message(subject, plaintext):
#     """
#     Send an information message to the users of the platform.
#     """
#     users = User.query.all()
#     # Only send email for activated accounts.
#     user_emails = [user.email for user in users if user.enabled]
#     # Postmark has a limit of twenty recipients per message in total.
#     for i in xrange(0, len(user_emails), 19):
#         emails.send(to=application.config['NOTIFICATION_EMAIL'],
#                     bcc=", ".join(user_emails[i:i+19]),
#                     subject=subject, plaintext=plaintext)


def new_request_notification(request):
    """
    New request notification.
    """
    plaintext = render_template('emails/new_request.txt', request=request)
    subject = "[{service}] New request".format(service=request.service.name)
    emails.send(to=request.email, subject=subject, plaintext=plaintext)
