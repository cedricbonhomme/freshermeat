
from flask import (Blueprint, render_template, redirect, flash, url_for)
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_args

from lib.utils import redirect_url
from web.views.common import admin_permission
from web import models

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard', defaults={'per_page': '10'},
                methods=['GET', 'POST'])
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
                            requests=requests.offset(offset).limit(per_page),
                            pagination=pagination)
