from datetime import datetime
from sqlalchemy import event
from freshermeat.bootstrap import db
from freshermeat.models import Project


class Release(db.Model):
    """Represent a release.
    """

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(), default="", nullable=False)
    state = db.Column(db.String(), default="")  # ie: stable
    scope = db.Column(db.String(), default="")  # ie: minor bugfix feature
    changes = db.Column(db.String(), default="")
    release_url = db.Column(db.String(), default="")
    download_url = db.Column(db.String(), default="")
    published_at = db.Column(db.DateTime(), default=datetime.utcnow())

    # foreign keys
    project_id = db.Column(db.Integer(), db.ForeignKey("project.id"), default=None)


@event.listens_for(Release, "after_insert")
def my_after_update_listener(mapper, connection, target):
    project_table = Project.__table__
    connection.execute(
        project_table.update()
        .where(project_table.c.id == target.project_id)
        .values(last_updated=datetime.utcnow())
    )
