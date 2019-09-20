from app import app
import unittest


class FlaskTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # check for login page loads correctly
    def test_login_page_load(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue('Please login' in response.data)

    # check if login behaves as expected with the correct  credentials 'admin'
    def test_login_with_admin_credentials(self):
        tester = app.test_client(self)
        response = tester.post('/login',
                               data=dict(username="admin", password="admin"),
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('logged in' in response.data)
        # import ipdb; ipdb.set_trace()

    # check if login behaves as expected with the incorrect  credentials 'admin'
    def test_login_with_incorrect_credentials(self):
        tester = app.test_client(self)
        response = tester.post('/login',
                               data=dict(username="blah", password="blah"),
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Invalid Credentials' in response.data)

    # ensure logout behaves correctly
    def test_user_logout(self):
        tester = app.test_client(self)
        response = tester.post('/login',
                               data=dict(username="admin", password="admin"),
                               follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('You logged out' in response.data)


if __name__ == '__main__':
    unittest.main()
