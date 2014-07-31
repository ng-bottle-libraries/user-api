from unittest import TestCase, main as unittest_main

from webtest import TestApp
from namespace_utils import test_funs as test

from namespace_user_api import oauth2_app as oauth2_bottle_app, user_api


class TestUserApi(TestCase):
    app = TestApp(user_api)
    oauth2_app = TestApp(oauth2_bottle_app)
    users = ({'email': 'foo@bar.com', 'password': 'bar'},
             {'email': 'foibal@bar.com', 'password': 'haz'},
             {'email': 'bar@foo.com', 'password': 'can'})
    access_token = ''

    @classmethod
    def setUpClass(cls):
        register_or_login_resp = cls.oauth2_app.put('/api/oauth2/register_or_login', cls.users[0])
        test.assertEqual(register_or_login_resp.content_type, 'application/json')
        test.assertEqual(register_or_login_resp.status_code, 200)
        test.assertIn('access_token', register_or_login_resp.json)
        test.assertIn('expires_in', register_or_login_resp.json)
        cls.access_token = register_or_login_resp.json['access_token']

    def test_get_profile_failure(self):
        k = 'access_token'
        self.assertNotEqual(self.app.get('/api/v1/user', {k: getattr(TestUserApi, k)}).json,
                            {'user': self.users[1]['email']})

    def test_get_profile_success(self):
        k = 'access_token'
        self.assertEqual(self.app.get('/api/v1/user', {k: getattr(TestUserApi, k)}).json,
                         {'user': self.users[0]['email']})

    @classmethod
    def tearDownClass(cls):
        unregister_resp = cls.oauth2_app.delete('/api/oauth2/unregister', params=cls.users[0])
        test.assertEqual(got=unregister_resp.content_type, expect=None)


if __name__ == '__main__':
    unittest_main()
