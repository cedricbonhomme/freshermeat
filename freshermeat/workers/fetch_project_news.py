#! /usr/bin/env python
import logging
from datetime import datetime
from time import mktime

import feedparser
from sqlalchemy import and_

from freshermeat.bootstrap import db
from freshermeat.models import News

logger = logging.getLogger(__name__)


def retrieve(feeds):
    """
    Launch the processus.
    """
    # Launch the process for all the feeds
    logger.info("Retrieving news...")
    for feed in feeds:
        try:
            data = feedparser.parse(feed.link)
        except Exception:
            continue
        for entry in data["entries"]:

            exist = News.query.filter(
                and_(News.entry_id == entry.id, News.project_id == feed.project_id)
            ).count()

            if exist:
                continue

            try:
                date = datetime.fromtimestamp(mktime(entry.published_parsed))
            except Exception:
                date = datetime.utcnow()

            new_news = News(
                entry_id=entry.id,
                link=entry.link,
                title=entry.title,
                content=entry.description,
                published=date,
                feed_id=feed.id,
                project_id=feed.project_id,
            )

            db.session.add(new_news)
        db.session.commit()
