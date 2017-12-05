from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

from bootstrap import db
from web.models import Project, Organization
from web.forms import AddProjectForm

project_bp = Blueprint('project_bp', __name__, url_prefix='/project')
projects_bp = Blueprint('projects_bp', __name__, url_prefix='/projects')


@projects_bp.route('/', methods=['GET'])
def list_projects():
    return render_template('projects.html')


@project_bp.route('/<string:project_name>', methods=['GET'])
def get(project_name=None):
    return render_template('project.html')


@project_bp.route('/create', methods=['GET'])
@project_bp.route('/edit/<int:project_id>', methods=['GET'])
@login_required
def form(project_id=None):
    action = "Add a project"
    head_titles = [action]

    form = AddProjectForm()
    form.organization_id.choices = [(org.id, org.name) for org in
                                    Organization.query.all()]

    if project_id is None:
        return render_template('edit_project.html', action=action,
                               head_titles=head_titles, form=form)
    project = Project.query.filter(Project.id == project_id).first()
    form = AddProjectForm(obj=project)
    form.organization_id.choices = [(org.id, org.name) for org in
                                    Organization.query.all()]
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
    form.organization_id.choices = [(org.id, org.name) for org in
                                    Organization.query.all()]

    if not form.validate():
        return render_template('edit_project.html', form=form)

    if project_id is not None:
        project = Project.query.filter(Project.id == project_id).first()
        form.populate_obj(project)
        db.session.commit()
        flash('Project {project_name} successfully updated.'.
              format(project_name=form.name.data), 'success')
        return redirect(url_for('project_bp.form', project_id=project.id))

    # Create a new project
    new_project = Project(name=form.name.data,
                          short_description=form.short_description.data,
                          description=form.description.data,
                          website=form.website.data)
    db.session.add(new_project)
    db.session.commit()
    flash('Project {project_name} successfully created.'.
          format(project_name=new_project.name), 'success')

    return redirect(url_for('project_bp.form', project_id=new_project.id))
