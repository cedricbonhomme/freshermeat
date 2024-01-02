#! /usr/bin/env python
# Freshermeat - An open source software directory and release tracker.
# Copyright (C) 2017-2024 Cédric Bonhomme - https://www.cedricbonhomme.org
#
# For more information: https://sr.ht/~cedric/freshermeat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from flask import abort
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from werkzeug.security import generate_password_hash

from freshermeat.bootstrap import db
from freshermeat.models import User
from freshermeat.web.forms import ProfileForm

user_bp = Blueprint("user_bp", __name__, url_prefix="/user")


@user_bp.route("/<string:login>", methods=["GET"])
def get(login=None):
    user = User.query.filter(User.login == login).first()
    if user is None:
        abort(404)
    return render_template("user.html", user=user)


@user_bp.route("/profile", methods=["GET"])
@login_required
def form():
    """Returns a form for the creation/edition of users."""
    user = User.query.filter(User.id == current_user.id).first()
    form = ProfileForm(obj=user)
    form.populate_obj(current_user)
    action = "Edit user"
    head_titles = [action]
    head_titles.append(user.login)
    return render_template(
        "edit_user.html", action=action, head_titles=head_titles, form=form, user=user
    )


@user_bp.route("/profile", methods=["POST"])
@login_required
def process_form():
    """Process the form for the creation/edition of users."""
    form = ProfileForm()

    if not form.validate():
        return render_template("edit_user.html", form=form)

    user = User.query.filter(User.id == current_user.id).first()
    form.populate_obj(user)
    if form.password.data:
        user.pwdhash = generate_password_hash(form.password.data)
    db.session.commit()
    # flash(User %(user_login)s successfully updated.',
    #         user_login=form.login.data, 'success')
    return redirect(url_for("user_bp.form"))


@user_bp.route("/generate_apikey", methods=["GET"])
@login_required
def generate_apikey():
    """Generate an API key for a user."""
    user = User.query.filter(User.id == current_user.id).first()
    if user is None:
        abort(404)
    user.generate_apikey()
    db.session.commit()
    flash("New API key generated.", "success")
    return redirect(url_for("user_bp.form"))
