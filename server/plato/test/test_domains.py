import json

from plato import db
from plato.model.user import User
from plato.test.base import BaseTestCase
from plato.test.utils import add_user, add_domain


class TestDomainService(BaseTestCase):
    def test_add_domain(self):
        '''Ensure a new domain can be added to database'''
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/domains',
                data=json.dumps(dict(
                    domain='www.baidu.com',
                    ip='http://111.13.100.91/',
                    master=1
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('www.baidu.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_duplicate_domain(self):
        '''Ensure error is thrown if user's email already exists'''
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            self.client.post(
                '/domains',
                data=json.dumps(dict(
                    domain='www.baidu.com',
                    ip='http://111.13.100.91/',
                    master=1
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            response = self.client.post(
                '/domains',
                data=json.dumps(dict(
                    domain='www.baidu.com',
                    ip='http://111.13.100.91/',
                    master=1
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry, that domain already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_domain_invalid_ip(self):
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/domains',
                data=json.dumps(dict(
                    domain='www.baidu.com',
                    master=1
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_domain_invalid_payload(self):
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/domains',
                data=json.dumps(dict(
                    ip='http://111.13.100.91/',
                    master=1
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_domain_invalid_master(self):
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/domains',
                data=json.dumps(dict(
                    domain='www.baidu.com',
                    ip='http://111.13.100.91/',
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_domain(self):
        '''Ensure get single user behaves correctly'''
        domain = add_domain('www.baidu.com', 'http://10.0.0.122', 1)
        with self.client:
            response = self.client.get(f'/domain/{domain.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('www.baidu.com', data['data']['domain'])
            self.assertIn('http://10.0.0.122', data['data']['ip'])
            self.assertIn('success', data['status'])

    def test_single_domain_no_id(self):
        '''Ensure error is thrown if an id is not provided'''
        with self.client:
            response = self.client.get('domain/test_id')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Domain does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_domain_incorrect_id(self):
        '''Ensure error is thrown if the id is not correct'''
        with self.client:
            response = self.client.get('domain/666')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Domain does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_not_admin(self):
        add_user('test', 'test@test.com', 'test')
        user = User.query.filter_by(email='test@test.com').first()
        user.admin = True
        db.session.commit()
        with self.client:
            # user login
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/domains',
                data=json.dumps(dict(
                    domain='www.baidu.com',
                    ip='http://111.13.100.91/',
                    master=1
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'You have no permission to do that.')
            self.assertEqual(response.status_code, 403)

    def test_all_domains(self):
        add_domain('www.baidu.com', 'http://111.13.100.91/', 1)
        add_domain('www.google.com', 'http://111.13.100.92/', 1)
        with self.client:
            response = self.client.get('/domains')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['domains']), 2)
            self.assertIn('www.google.com', data['data']['domains'][0]['domain'])
            self.assertIn('www.baidu.com', data['data']['domains'][1]['domain'])
            self.assertIn('http://111.13.100.92/', data['data']['domains'][0]['ip'])
            self.assertIn('http://111.13.100.91/', data['data']['domains'][1]['ip'])
