
from flask import Blueprint, render_template, redirect, url_for, current_app, \
                flash, request
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_args
from sqlalchemy import desc
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink

from web.views.common import admin_permission
from notifications.notifications import new_request_notification
from bootstrap import db
from web import models

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard', defaults={'per_page': '10'}, methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def dashboard(per_page):
    organization_name = request.args.get('org', False)

    requests = models.Request.query
    if organization_name:
        requests = requests.filter(models.Request.project.has(
                                   organization=organization_name))

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


# Flask-Admin views

class UserView(ModelView):
    column_exclude_list = ['pwdhash']
    column_editable_list = ['email', 'firstname', 'lastname']
    can_create = False

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


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
                    # template_mode='bootstrap3',
                    base_template='layout.html',
                    index_view=CustomAdminIndexView(
                        name='Home',
                        url='/admin'
                    ))
admin_flask.add_view(UserView(models.User, db.session))
admin_flask.add_view(ProjectView(models.Project, db.session))
admin_flask.add_link(menu_link_back_dashboard)
