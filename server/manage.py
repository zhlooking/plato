import unittest

import coverage
from flask_migrate import MigrateCommand
from flask_script import Manager

from plato import create_app, db
from plato.model.user import User
from plato.model.domain import Domain


COV = coverage.coverage(
    branch=True,
    include='plato/*',
    omit=[
        'plato/tests/*',
        'plato/__init__.py'
        'plato/config.py',
    ]
)
COV.start()


app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    ''' Run tests without code coverage '''
    tests = unittest.TestLoader().discover('plato/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    '''run the unittest with coverage'''
    tests = unittest.TestLoader().discover('plato/test')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def seed_db():
    '''Seeds the database'''
    db.session.add(User('michael', 'michael@.com', 'test_pwd'))
    db.session.add(User('michaelherman', 'michaelherman@realpython.com', 'test_pwd'))
    db.session.add(Domain('www.baidu.com', 'http://10.0.0.100', 1))
    db.session.add(Domain('www.google.com', 'http://10.0.0.200', 1))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
