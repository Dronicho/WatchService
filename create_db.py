#!flask/bin/python
import os.path

from migrate.versioning import api

from app import db, api as app_api, app

SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']
SQLALCHEMY_MIGRATE_REPO = app.config['SQLALCHEMY_MIGRATE_REPO']


def bootstrap(scheduler):
    db.create_all()
    try:
        if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
            api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
            api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
        else:
            api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
    except Exception as e:
        print('Something happened')

    try:
        scheduler.add_job(app_api.Covid().get_info, 'interval', id='covid_job',
                          minutes=app.config['REQUEST_INTERVAL'])
        scheduler.add_job(app_api.Currencies().get_info, 'interval', id='currencies_job',
                          minutes=app.config['REQUEST_INTERVAL'])
    except Exception as e:
        print('Jobs already created')

