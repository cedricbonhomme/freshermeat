#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Freshermeat - An open source software directory and release tracker.
# Copyright (C) 2017-2022 Cédric Bonhomme - https://www.cedricbonhomme.org
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

from flask import url_for, redirect
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    PasswordField,
    BooleanField,
    SelectField,
    SubmitField,
    validators,
    HiddenField,
    SelectMultipleField,
)
from flask_wtf.file import FileField
from wtforms.fields import URLField
from wtforms.validators import url
from wtforms.validators import InputRequired

from freshermeat.lib import misc_utils
from freshermeat.models import Project, User, Organization, License, Language


class RedirectForm(FlaskForm):
    """
    Secure back redirects with WTForms.
    """

    next = HiddenField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = misc_utils.get_redirect_target() or ""

    def redirect(self, endpoint="services", **values):
        if misc_utils.is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = misc_utils.get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


class SigninForm(RedirectForm):
    """
    Sign in form.
    """

    login = StringField(
        "Login",
        [
            validators.Length(min=3, max=30),
            InputRequired("Please enter your login."),
        ],
    )
    password = PasswordField(
        "Password",
        [
            InputRequired("Please enter a password."),
            validators.Length(min=6, max=100),
        ],
    )
    submit = SubmitField("Log In")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        validated = super().validate()
        user = User.query.filter(User.login == self.login.data).first()
        if not user:
            self.login.errors.append("Impossible to login.")
            validated = False
        else:
            if not user.is_active:
                self.login.errors.append("Impossible to login.")
                validated = False
            if not user.check_password(self.password.data):
                self.password.errors.append("Impossible to login.")
                validated = False
            self.user = user
        return validated


class AddProjectForm(FlaskForm):
    name = StringField("Name", [InputRequired("Please enter a name")])
    description = TextAreaField("Description", [validators.Optional()])
    short_description = StringField(
        "Short description", [InputRequired("Please enter a short description")]
    )
    website = StringField("Website", [validators.Optional()])
    licenses = SelectMultipleField(
        "Licenses", [InputRequired("Please choose a license")], coerce=int
    )
    languages = SelectMultipleField("Languages", [validators.Optional()], coerce=int)
    dependencies = SelectMultipleField(
        "Dependencies", [validators.Optional()], coerce=int
    )
    dependents = SelectMultipleField("Dependents", [validators.Optional()], coerce=int)
    tags = StringField("Tags")
    organization_id = SelectField("Organization", [validators.Optional()], coerce=int)
    organization_id.choices = [(0, "")]
    organization_id.choices.extend(
        [(org.id, org.name) for org in Organization.query.all()]
    )
    logo = FileField("Logo")

    automatic_release_tracking = StringField(
        "Automatic Release Tracking", [validators.Optional()]
    )

    cve_vendor = StringField("CVE vendor", [validators.Optional()])
    cve_product = StringField("CVE product", [validators.Optional()])

    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dependencies.choices = [
            (project.id, project.name) for project in Project.query.all()
        ]
        self.dependents.choices = [
            (project.id, project.name) for project in Project.query.all()
        ]
        self.licenses.choices = [
            (license.id, license.name) for license in License.query.all()
        ]
        self.languages.choices = [
            (language.id, language.name) for language in Language.query.all()
        ]


class AddOrganizationForm(FlaskForm):
    name = StringField("Name", [InputRequired("Please enter a name")])
    description = TextAreaField(
        "Description", [InputRequired("Please enter a description")]
    )
    short_description = StringField(
        "Short description", [InputRequired("Please enter a short description")]
    )
    website = StringField("Website", [validators.Optional()])
    organization_type = StringField("Organization type", [validators.Optional()])
    cve_vendor = StringField("CVE vendor", [validators.Optional()])
    logo = FileField("Logo")
    submit = SubmitField("Save")


class UserForm(FlaskForm):
    """
    Create or edit a user (for the administrator).
    """

    login = StringField(
        "Login",
        [
            validators.Length(min=3, max=30),
            InputRequired("Please enter your login."),
        ],
    )
    password = PasswordField("Password")
    public_profile = BooleanField("Public profile", default=True)
    is_active = BooleanField("Active", default=True)
    is_admin = BooleanField("Admin", default=False)
    is_api = BooleanField("API", default=False)
    submit = SubmitField("Save")


class ProfileForm(FlaskForm):
    """
    Edit a profile.
    """

    login = StringField(
        "Login",
        [
            validators.Length(min=3, max=30),
            InputRequired("Please enter your login."),
        ],
    )
    password = PasswordField("Password")
    public_profile = BooleanField("Public profile", default=True)
    submit = SubmitField("Save")


class CodeForm(FlaskForm):
    """
    Management of code locations.
    """

    repository_url = StringField(
        "Repository URL", [InputRequired("Please enter a repository URL.")]
    )
    scm_type = SelectField(
        "Repository type",
        [InputRequired()],
        coerce=str,
        choices=[
            ("Git", "Git"),
            ("Mercurial", "Mercurial"),
            ("Bazaar", "Bazaar"),
            ("Fossil", "Fossil"),
            ("Subversion", "Subversion"),
        ],
    )
    submit = SubmitField("Save")


class FeedForm(FlaskForm):
    """
    Management of feed locations.
    """

    link = StringField("Feed URL", [InputRequired("Please enter a feed URL.")])
    submit = SubmitField("Save")


class SubmissionForm(FlaskForm):
    """
    Create a submission.
    """

    project_name = StringField("Name", [InputRequired("Please enter a name.")])
    project_description = TextAreaField("Description", [validators.Optional()])
    project_website = URLField(
        "Website", [InputRequired("Please enter a Website."), url()]
    )
    licenses = SelectMultipleField(
        "Licenses", [InputRequired("Please choose a license")], coerce=int
    )
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.licenses.choices = [
            (license.id, license.name) for license in License.query.all()
        ]
