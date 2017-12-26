
from flask import Blueprint, render_template, redirect, url_for, current_app, \
                flash, request
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

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard', defaults={'per_page': '10'}, methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def dashboard(per_page):
    organization_name = request.args.get('org', False)

    requests = models.Request.query
    if organization_name:
        orga = models.Organization.query.filter(models.Organization.name == organization_name).first()
        if orga:
            requests = requests.filter(models.Request.project.has(
                                       organization_id=orga.id))

    page, per_page, offset = get_page_args()
    pagination = Pagination(page=page, total=requests.count(),
                            css_framework='bootstrap4',
                            search=False, record_name='requests',
                            per_page=per_page)

    return render_template('admin/dashboard.html', requests=requests.order_by(
                           desc(models.Request.created_at)
                           ).offset(offset).limit(per_page),
                           pagination=pagination)


@admin_bp.route('/request/<request_id>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def view_request(request_id=None):
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
    """Delete a request."""
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
    """Mark a request as unchecked."""
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
        print(e)
    return redirect(url_for('admin_bp.view_request', request_id=req.id))


@admin_bp.route('/users', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def list_users():
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
    head_titles.append(user.email)
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
        flash('User {user_nickname} successfully updated.'.
              format(user_nickname=form.nickname.data), 'success')
        return redirect(url_for('admin_bp.form_user', user_id=user.id))

    # Create a new user
    new_user = models.User(nickname=form.nickname.data,
                           email=form.email.data,
                           public_profile=form.public_profile.data,
                           is_active=form.is_active.data,
                           is_admin=form.is_admin.data,
                           is_api=form.is_api.data,
                           pwdhash=generate_password_hash(form.password.data))
    db.session.add(new_user)
    db.session.commit()
    flash('User {user_email} successfully created.'.
          format(user_email=new_user.email), 'success')

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

class ProjectView(ModelView):
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
admin_flask.add_view(ProjectView(models.Project, db.session))
admin_flask.add_link(menu_link_back_dashboard)
