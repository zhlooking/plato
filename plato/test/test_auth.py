import time
import json

from plato.test.utils import add_user
from plato.test.base import BaseTestCase
from plato.api.models import User
from plato import db


class TestAuthService(BaseTestCase):

    def test_user_registration(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='foo',
                    email='foo@bar.com',
                    password='test_pwd'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered')
            self.assertTrue(data['auth_token'] is not None)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_email(self):
        add_user('foo', 'foo@bar.com', 'test_pwd')
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='bar',
                    email='foo@bar.com',
                    password='test_pwd'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'error')
            self.assertIn('Sorry. That user already exists', data['message'])

    def test_user_registeration_duplicate_username(self):
        add_user('foo', 'foo@bar.com', 'test_pwd')
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='foo',
                    email='foo@foo.com',
                    password='test_pwd'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'error')
            self.assertIn('Sorry. That user already exists', data['message'])

    def test_user_registeration_valid_json(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict()),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertTrue(data['status'] == 'error')

    def test_user_registeration_invalid_json_keys_no_username(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    email='foo@foo.com',
                    password='test_pwd'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'error')
            self.assertIn('Invalid payload', data['message'])

    def test_user_registeration_invalid_json_keys_no_email(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='foo',
                    password='test_pwd'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'error')
            self.assertIn('Invalid payload', data['message'])

    def test_user_registeration_invalid_json_keys_no_password(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='foo',
                    email='foo@foo.com',
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertTrue(data['status'] == 'error')
            self.assertIn('Invalid payload', data['message'])

    def test_registered_user_login(self):
        with self.client:
            _ = add_user('foo', 'foo@bar.com', 'test_pwd')
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='foo@bar.com',
                    password='test_pwd'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'Successfully logged in')
            self.assertTrue(data['auth_token'] is not None)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_not_registered_user_login(self):
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='foo@bar.com',
                    password='test_pwd'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'error')
            self.assertEqual(data['message'], 'User does not exists')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_valid_logout(self):
        add_user('foo', 'foo@bar.com', 'test_pwd')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='foo@bar.com',
                    password='test_pwd'
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out')

    def test_invalid_logout_expired_token(self):
        add_user('foo', 'foo@bar.com', 'test_pwd')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='foo@bar.com',
                    password='test_pwd'
                )),
                content_type='application/json'
            )
            # invalid token logout
            time.sleep(4)
            response = self.client.get(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout_inactive(self):
        add_user('foo', 'foo@bar.com', 'test_pwd')
        user = User.query.filter_by(email='foo@bar.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='foo@bar.com',
                    password='test_pwd'
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Something went wrong. Please contact us.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout(self):
        with self.client:
            response = self.client.get(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer invalid'
                ),
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'Invalid token. Please log in again.')
            self.assertTrue(response.status_code, 401)

    def test_auth_status(self):
        add_user('foo', 'foo@bar.com', 'test_pwd')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='foo@bar.com',
                    password='test_pwd'
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(resp_login.data.decode())['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == 'foo')
            self.assertTrue(data['data']['email'] == 'foo@bar.com')
            self.assertTrue(data['data']['active'] is True)
            self.assertTrue(data['data']['created_at'] is not None)
            self.assertEqual(response.status_code, 200)

    def test_invalid_status(self):
        with self.client:
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer invalid'
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'Invalid token. Please log in again.')
            self.assertTrue(response.status_code, 401)

    def test_invalid_status_inactive(self):
        # add_user('foo', 'foo@bar.com', 'test_pwd')
        # user = User.query.filter_by(email='foo@bar.com').first()
        # user.active = False
        # db.session.commit()
        # with self.client:
        #     resp_login = self.client.post(
        #         '/auth/login',
        #         data=json.dumps(dict(
        #             email='foo@bar.com',
        #             password='test_pwd'
        #         )),
        #         content_type='application/json'
        #     )
        #     response = self.client.get(
        #         '/auth/status',
        #         headers=dict(
        #             Authorization='Bearer ' + json.loads(resp_login.data.decode())['auth_token']
        #         )
        #     )
        #     data = json.loads(response.data.decode())
        #     self.assertTrue(data['status'] == 'error')
        #     self.assertTrue(data['message'] == 'Something went wrong. Please contact us.')
        #     self.assertTrue(response.status_code, 401)

        add_user('test', 'test@test.com', 'test')
        # update user
        user = User.query.filter_by(email='test@test.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Something went wrong. Please contact us.')
            self.assertEqual(response.status_code, 401)
