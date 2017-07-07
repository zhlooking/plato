from plato import db


class Domain(db.Model):
    __tablename__ = 'domains'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain = db.Column(db.String(128), unique=True, nullable=False)
    ip = db.Column(db.String(128), unique=True, nullable=False)
    master = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, domain, ip, master):
        self.domain = domain
        self.ip = ip
        self.master = master
