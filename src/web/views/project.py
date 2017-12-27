import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from werkzeug.contrib.atom import AtomFeed

from bootstrap import db, application
from web.models import get_or_create, Project, Organization, Tag, Icon, License
from web.forms import AddProjectForm
from web.utils import misc

project_bp = Blueprint('project_bp', __name__, url_prefix='/project')
projects_bp = Blueprint('projects_bp', __name__, url_prefix='/projects')


@projects_bp.route('/', methods=['GET'])
def list_projects():
    return render_template('projects.html')


@project_bp.route('/<string:project_name>', methods=['GET'])
def get(project_name=None):
    project = Project.query.filter(Project.name == project_name).first()
    return render_template('project.html', project=project)


@project_bp.route('/<string:project_name>/releases.atom', methods=['GET'])
def recent_releases(project_name=None):
    """Generates a feed for the releases."""
    feed = AtomFeed('Recent releases',
                     feed_url=request.url, url=request.url_root)
    project = Project.query.filter(Project.name == project_name).first()
    for release in project.releases:
        feed.add(release.version, release.changes,
                 id=release.id,
                 url=release.release_url,
                 updated=release.published_at)
    return feed.get_response()


@project_bp.route('/create', methods=['GET'])
@project_bp.route('/edit/<int:project_id>', methods=['GET'])
@login_required
def form(project_id=None):
    action = "Add a project"
    head_titles = [action]

    form = AddProjectForm()
    form.organization_id.choices = [(0, '')]
    form.organization_id.choices.extend([(org.id, org.name) for org in
                                                    Organization.query.all()])

    if project_id is None:
        return render_template('edit_project.html', action=action,
                               head_titles=head_titles, form=form)
    project = Project.query.filter(Project.id == project_id).first()
    form = AddProjectForm(obj=project)
    form.organization_id.choices = [(0, '')]
    form.organization_id.choices.extend([(org.id, org.name) for org in
                                            Organization.query.all()])
    form.licenses.data = [license.id for license in
                                            project.licenses]
    form.tags.data = ", ".join(project.tags)
    action = "Edit project"
    head_titles = [action]
    head_titles.append(project.name)
    return render_template('edit_project.html', action=action,
                           head_titles=head_titles,
                           form=form, project=project)


@project_bp.route('/create', methods=['POST'])
@project_bp.route('/edit/<int:project_id>', methods=['POST'])
@login_required
def process_form(project_id=None):
    form = AddProjectForm()
    form.organization_id.choices = [(0, '')]
    form.organization_id.choices.extend([(org.id, org.name) for org in
                                                    Organization.query.all()])

    if not form.validate():
        return render_template('edit_project.html', form=form)

    if form.organization_id.data == 0:
        form.organization_id.data = None

    if project_id is not None:
        project = Project.query.filter(Project.id == project_id).first()

        # Tags
        new_tags = [tag for tag in form.tags.data.strip().split(',') if tag]
        for tag in project.tag_objs:
            if tag.text not in new_tags:
                db.session.delete(tag)
        db.session.commit()
        for tag in new_tags:
            get_or_create(db.session, Tag, **{'text': tag.strip(),
                                              'project_id': project.id})
        del form.tags

        # Licenses
        new_licenses = []
        for license_id in form.licenses.data:
            license = License.query.filter(License.id == license_id).first()
            new_licenses.append(license)
        project.licenses = new_licenses
        del form.licenses

        # Logo
        f = form.logo.data
        if f:
            try:
                # Delete the previous icon
                icon_url = os.path.join(application.config['UPLOAD_FOLDER'],
                                        project.icon_url)
                os.unlink(icon_url)
                old_icon = Icon.query.filter(Icon.url == project.icon_url) \
                                     .first()
                db.session.delete(old_icon)
                project.icon_url = None
                db.session.commit()
            except Exception as e:
                print(e)

            # save the picture
            filename = str(uuid.uuid4()) + '.png'
            icon_url = os.path.join(application.config['UPLOAD_FOLDER'],
                                    filename)
            f.save(icon_url)
            # create the corresponding new icon object
            new_icon = Icon(url=filename)
            db.session.add(new_icon)
            db.session.commit()
            project.icon_url = new_icon.url


        form.populate_obj(project)
        db.session.commit()
        flash('Project {project_name} successfully updated.'.
              format(project_name=form.name.data), 'success')
        return redirect(url_for('project_bp.form', project_id=project.id))


    # Create a new project
    new_project = Project(name=form.name.data,
                          short_description=form.short_description.data,
                          description=form.description.data,
                          website=form.website.data,
                          organization_id=form.organization_id.data)
    db.session.add(new_project)
    db.session.commit()
    # Tags
    for tag in form.tags.data.split(','):
        get_or_create(db.session, Tag, **{'text': tag.strip(),
                                          'project_id': new_project.id})

    # Licenses
    new_licenses = []
    for license_id in form.licenses.data:
        license = License.query.filter(License.id == license_id).first()
        new_licenses.append(license)
    new_project.licenses = new_licenses
    del form.licenses

    # Logo
    f = form.logo.data
    if f:
        # save the picture
        filename = str(uuid.uuid4()) + '.png'
        icon_url = os.path.join(application.config['UPLOAD_FOLDER'],
                                filename)
        f.save(icon_url)
        # create the corresponding new icon object
        new_icon = Icon(url=filename)
        db.session.add(new_icon)
        new_project.icon_url = new_icon.url
    db.session.commit()
    flash('Project {project_name} successfully created.'.
          format(project_name=new_project.name), 'success')

    return redirect(url_for('project_bp.form', project_id=new_project.id))
