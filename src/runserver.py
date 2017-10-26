#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bootstrap import application, populate_g

with application.app_context():
    populate_g()

    from web import views
    application.register_blueprint(views.admin_bp)
    # application.register_blueprint(views.users_bp)
    # application.register_blueprint(views.user_bp)

    # API v1
    application.register_blueprint(views.api.v1.blueprint_service)
    application.register_blueprint(views.api.v1.blueprint_request)


if __name__ == '__main__':
    application.run(host=application.config['HOST'],
                    port=application.config['PORT'])
