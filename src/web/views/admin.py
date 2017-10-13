
from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_args
from sqlalchemy import desc
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink

from web.views.common import admin_permission
from bootstrap import db
from web import models

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard', defaults={'per_page': '10'}, methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def dashboard(per_page):
    requests = models.Request.query

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
def request(request_id=None):
    request = models.Request.query.filter(models.Request.id == request_id). \
                                                                        first()
    if request.required_informations is None:
        request.required_informations = {}

    if not request.checked:
        request.checked = True
        db.session.commit()

    return render_template('admin/request.html', request=request)


# Flask-Admin views

class UserView(ModelView):
    column_exclude_list = ['pwdhash']
    column_editable_list = ['email', 'firstname', 'lastname']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class ServiceView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


menu_link_back_dashboard = MenuLink(name='Dashboard',
                                    url='/admin/dashboard')

admin_flask = Admin(current_app,
                    name='Management of data',
                    template_mode='bootstrap3',
                    index_view=AdminIndexView(
                        name='Home',
                        url='/admin/data_management/'
                    ))
admin_flask.add_view(UserView(models.User, db.session))
admin_flask.add_view(ServiceView(models.Service, db.session))
admin_flask.add_link(menu_link_back_dashboard)
