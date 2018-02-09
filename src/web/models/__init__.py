#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .user import User
from .tag import Tag
from .project import Project
from .code import Code
from .license import License
from .organization import Organization
from .release import Release
from .cve import CVE
from .icon import Icon
from .request import Request
from .service import Service

__all__ = ['Project', 'License', 'Release', 'User',
           'Organization', 'Tag', 'Request', 'CVE',
           'Code', 'Service']

from sqlalchemy.engine import reflection
from sqlalchemy import create_engine
from sqlalchemy.schema import (MetaData,
                               Table,
                               DropTable,
                               ForeignKeyConstraint,
                               DropConstraint)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def db_create(db, db_config_dict, database_name):
    db_conn_format = "postgresql://{user}:{password}@{host}:{port}/{database}"
    db_conn_uri_default = (db_conn_format.format(
        database='postgres',
        **db_config_dict))
    engine_default = create_engine(db_conn_uri_default)
    conn = engine_default.connect()
    conn.execute("COMMIT")
    conn.execute("CREATE DATABASE %s" % database_name)
    conn.close()


def db_init(db):
    "Will create the database from conf parameters."
    db.create_all()


def db_empty(db):
    "Will drop every datas stocked in db."
    # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything
    conn = db.engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    with conn.begin() as trans:

        inspector = reflection.Inspector.from_engine(db.engine)

        # gather all data first before dropping anything.
        # some DBs lock after things have been dropped in
        # a transaction.
        metadata = MetaData()

        tbs = []
        all_fks = []

        for table_name in inspector.get_table_names():
            fks = []
            for fk in inspector.get_foreign_keys(table_name):
                if not fk['name']:
                    continue
                fks.append(ForeignKeyConstraint((), (), name=fk['name']))
            t = Table(table_name, metadata, *fks)
            tbs.append(t)
            all_fks.extend(fks)

        for fkc in all_fks:
            conn.execute(DropConstraint(fkc))

        for table in tbs:
            conn.execute(DropTable(table))

        trans.commit()
