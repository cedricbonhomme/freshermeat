#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import feedparser
from time import mktime
from datetime import datetime


from bootstrap import db
from web.models import News

logger = logging.getLogger(__name__)


def retrieve(feeds):
    """
    Launch the processus.
    """
    # Launch the process for all the projects
    logger.info('Retrieving news...')
    for feed in feeds:
        try:
            data = feedparser.parse(feed.link)
        except:
            continue
        for entry in data['entries']:

            exist = News.query. \
                    filter(News.entry_id==entry.id). \
                    count()

            if exist:
                continue

            try:
                date = datetime.fromtimestamp(mktime(entry.published_parsed))
            except:
                date = datetime.utcnow()

            new_news = News(entry_id=entry.id, link=entry.link,
                            title=entry.title,
                            content=entry.description,
                            published=date,
                            feed_id=feed.id,
                            project_id=feed.project_id)

            db.session.add(new_news)
        db.session.commit()
