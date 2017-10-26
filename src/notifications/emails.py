#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import conf
from lib.decorators import async

logger = logging.getLogger(__name__)


@async
def send_async_email(mfrom, mto, msg):
    try:
        s = smtplib.SMTP(conf.NOTIFICATION_HOST)
        s.login(conf.NOTIFICATION_USERNAME, conf.NOTIFICATION_PASSWORD)
    except Exception:
        logger.exception('send_async_email raised:')
    else:
        s.sendmail(mfrom, mto, msg.as_string())
        s.quit()


def send(*args, **kwargs):
    """
    This functions enables to send email through SendGrid
    or a SMTP server.
    """
    send_smtp(**kwargs)


def send_smtp(to="", bcc="", subject="", plaintext="", html=""):
    """
    Send an email.
    """
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = conf.NOTIFICATION_EMAIL
    msg['To'] = to
    msg['BCC'] = bcc

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(html, 'html', 'utf-8')
    part2 = MIMEText(plaintext, 'plain', 'utf-8')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the plaintext message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    try:
        s = smtplib.SMTP(conf.NOTIFICATION_HOST)
        s.login(conf.NOTIFICATION_USERNAME, conf.NOTIFICATION_PASSWORD)
    except Exception:
        logger.exception("send_smtp raised:")
    else:
        s.sendmail(conf.NOTIFICATION_EMAIL,
                   msg['To'] + ", " + msg['BCC'],
                   msg.as_string())
        s.quit()
