from plato.test.base import BaseTestCase
from sqlalchemy.exc import IntegrityError

from plato import db
from plato.model.domain import Domain
from plato.test.utils import add_domain


class TestDomainModel(BaseTestCase):
    def test_domain_model(self):
        domain = add_domain('www.baidu.com', '111.13.100.91', 1)
        self.assertTrue(domain.id)
        self.assertEqual('www.baidu.com', domain.domain)
        self.assertEqual('111.13.100.91', domain.ip)
        self.assertTrue(domain.master)

    def test_add_domain_duplicate_username(self):
        add_domain('www.baidu.com', '111.13.100.91', 2)
        duplicate_domain = Domain('www.baidu.com', '111.13.100.92', 2)
        db.session.add(duplicate_domain)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_ip_duplicate_email(self):
        add_domain('www.baidu.com', '111.13.100.91', 2)
        duplicate_domain = Domain('www.fake-baidu.com', '111.13.100.91', 2)
        db.session.add(duplicate_domain)
        self.assertRaises(IntegrityError, db.session.commit)
