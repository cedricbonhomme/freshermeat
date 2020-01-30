
from collections import Counter

from freshermeat.bootstrap import application
from freshermeat.models import Project, Tag

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in application['ALLOWED_EXTENSIONS']


def similar_projects(project):
    similar_counter = Counter()
    for tag in project.tags:
        res = Project.query.filter(Project.tags.any(Tag.text==tag),
                                    Project.id!=project.id).all()
        for similar in res:
            similar_counter[similar.name] += 1
    return similar_counter.most_common(5)
