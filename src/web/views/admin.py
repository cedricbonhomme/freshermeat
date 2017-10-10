
from flask import Blueprint, render_template
from flask_login import login_required
from flask_paginate import Pagination, get_page_args
from sqlalchemy import desc

from web.views.common import admin_permission
from bootstrap import db
from web import models

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


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

    return render_template('admin/dashboard.html',
                            requests=requests.order_by(desc(models.Request.created_at)).offset(offset).limit(per_page),
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
