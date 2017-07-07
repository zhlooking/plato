import datetime

from plato import db
from plato.model.user import User
from plato.model.domain import Domain


def add_user(username, email, password, created_at=datetime.datetime.now()):
    user = User(username=username, email=email, password=password, created_at=created_at)
    db.session.add(user)
    db.session.commit()
    return user


def add_domain(domain, ip, master):
    domain = Domain(domain=domain, ip=ip, master=master)
    db.session.add(domain)
    db.session.commit()
    return domain
