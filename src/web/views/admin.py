
import logging
from flask import Blueprint, render_template, redirect, url_for, current_app, \
                flash, request, abort
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_args
from sqlalchemy import desc
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from werkzeug import generate_password_hash

from web.views.common import admin_permission
from notifications.notifications import new_request_notification
from bootstrap import db
from web.forms import UserForm
from web import models

logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def dashboard():
    """Returns a simple dashboard for the administrators. This dashboard
    shows key figures (number of projects, releases, submissions, requests,
    users, etc.) about the platform."""
    nb_projects = models.Project.query.filter().count()
    nb_releases = models.Release.query.filter().count()
    nb_organizations = models.Organization.query.filter().count()
    nb_users = models.User.query.filter().count()
    nb_admin = models.User.query.filter(models.User.is_admin==True).count()
    nb_requests = models.Request.query.filter().count()
    nb_unique_tags = models.Tag.query.distinct(models.Tag.text).count()
    nb_submissions = models.Submission.query.filter().count()
    nb_pending_submissions = models.Submission.query.filter(
                                    models.Submission.reviewed==False).count()
    return render_template('admin/dashboard.html',
                           nb_projects=nb_projects, nb_releases=nb_releases,
                           nb_users=nb_users, nb_admin=nb_admin,
                           nb_requests=nb_requests,
                           nb_organizations=nb_organizations,
                           nb_unique_tags=nb_unique_tags,
                           nb_submissions=nb_submissions,
                           nb_pending_submissions=nb_pending_submissions)


@admin_bp.route('/requests', defaults={'per_page': '10'}, methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def requests(per_page):
    """Returns a page which displays a paginated lists of requests."""
    project_name = request.args.get('project', False)

    requests = models.Request.query
    if project_name:
        project = models.Project.query.filter(models.Project.name == project_name).first()
        if project:
            requests = [service.request for service in project.services]
            # requests = requests.filter(models.Service.project.has(
            #                            models.Project.name==project.name))

    page, per_page, offset = get_page_args()
    pagination = Pagination(page=page, total=requests.count(),
                            css_framework='bootstrap4',
                            search=False, record_name='requests',
                            per_page=per_page)

    return render_template('admin/requests.html', requests=requests.order_by(
                           desc(models.Request.created_at)
                           ).offset(offset).limit(per_page),
                           pagination=pagination)


@admin_bp.route('/request/<request_id>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def view_request(request_id=None):
    """Returns a page with details information about the request given if __name__ == '__main__':
    parameter."""
    request = models.Request.query.filter(models.Request.id == request_id). \
                                                                        first()
    if request.required_informations is None:
        request.required_informations = {}

    if not request.checked:
        request.checked = True
        db.session.commit()

    return render_template('admin/request.html', request=request)


@admin_bp.route('/request/<request_id>/delete', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def delete_request(request_id=None):
    """Let an administrator delete a request."""
    try:
        models.Request.query.filter(models.Request.id == request_id).delete()
        db.session.commit()
        flash('Request deleted.', 'info')
    except Exception as e:
        flash('Impossible to delete request.', 'danger')
        print(e)
    return redirect(url_for('admin_bp.dashboard'))


@admin_bp.route('/request/<request_id>/mark_as_unchecked', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def mark_as_unchecked(request_id=None):
    """Let an administrator mark a request as unchecked."""
    try:
        req = models.Request.query.filter(models.Request.id == request_id) \
                                  .first()
        models.Request.query.filter(models.Request.id == request_id) \
                            .update({'checked': not req.checked})
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect(url_for('admin_bp.dashboard'))


@admin_bp.route('/request/<request_id>/send_request_notification', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def send_request_notification(request_id=None):
    """Send a notification for the request."""
    req = None
    try:
        req = models.Request.query.filter(models.Request.id == request_id) \
                                  .first()
    except Exception as e:
        print(e)
    try:
        new_request_notification(req)
        req.notification_sent = True
        db.session.commit()
        flash('Email sent.', 'info')
    except Exception as e:
        flash('Impossible to send email.', 'danger')
        logger.exception('send_request_notification: ' + str(e))
    return redirect(url_for('admin_bp.view_request', request_id=req.id))


@admin_bp.route('/users', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def list_users():
    """Returns to an administrator a page which displays the list of users."""
    users = models.User.query.all()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/user/create', methods=['GET'])
@admin_bp.route('/user/edit/<int:user_id>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def form_user(user_id=None):
    action = "Add a user"
    head_titles = [action]
    form = UserForm()
    if user_id is None:
        return render_template('admin/edit_user.html', action=action,
                               head_titles=head_titles, form=form)

    user = models.User.query.filter(models.User.id == user_id).first()
    form = UserForm(obj=user)
    action = "Edit user"
    head_titles = [action]
    head_titles.append(user.login)
    return render_template('admin/edit_user.html', action=action,
                           head_titles=head_titles,
                           form=form, user=user)


@admin_bp.route('/user/create', methods=['POST'])
@admin_bp.route('/user/edit/<int:user_id>', methods=['POST'])
@login_required
def process_user_form(user_id=None):
    form = UserForm()

    if not form.validate():
        return render_template('admin/edit_user.html', form=form)

    if user_id is not None:
        user = models.User.query.filter(models.User.id == user_id).first()
        form.populate_obj(user)
        if form.password.data:
            user.pwdhash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('User {user_login} successfully updated.'.
              format(user_login=form.login.data), 'success')
        return redirect(url_for('admin_bp.form_user', user_id=user.id))

    # Create a new user
    new_user = models.User(login=form.login.data,
                           public_profile=form.public_profile.data,
                           is_active=form.is_active.data,
                           is_admin=form.is_admin.data,
                           is_api=form.is_api.data,
                           pwdhash=generate_password_hash(form.password.data))
    db.session.add(new_user)
    db.session.commit()
    flash('User {user_login} successfully created.'.
          format(user_login=new_user.login), 'success')

    return redirect(url_for('admin_bp.form_user', user_id=new_user.id))


@admin_bp.route('/user/delete/<int:user_id>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def delete_user(user_id=None):
    pass


@admin_bp.route('/user/toggle/<int:user_id>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def toggle_user(user_id=None):
    pass



# Flask-Admin views

class SecureView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


menu_link_back_dashboard = MenuLink(name='Dashboard',
                                    url='/admin/dashboard')
admin_flask = Admin(current_app,
                    name='Management of data',
                    template_mode='bootstrap3',
                    index_view=CustomAdminIndexView(
                        name='Home',
                        url='/admin'
                    ))
admin_flask.add_view(SecureView(models.Project, db.session))
admin_flask.add_view(SecureView(models.Organization, db.session))
admin_flask.add_view(SecureView(models.License, db.session))
admin_flask.add_view(SecureView(models.Language, db.session))
admin_flask.add_view(SecureView(models.Service, db.session))
admin_flask.add_link(menu_link_back_dashboard)
