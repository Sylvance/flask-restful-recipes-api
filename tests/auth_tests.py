import json
from tests.base_test_case import BaseTestCase

class AuthTestCases(BaseTestCase):
    """
    Tests for the authentication blueprint
    """
    def test_get_users(self):
        """ 
            A test for retrieving list of users
            The url endpoint is;
                =>    /api/users (get)
        """
        response = self.tester.get('/api/users',
                                    headers=dict(Authorization='Bearer ' + self.token), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_create_new_user(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /api/users (post)
        """
        new_user_data = json.dumps(dict({
            "username" : "Juma",
            "first_name" : "Juma",
            "last_name" : "Mwangi",
            "email" : "juma@gmail.com",
            "password" : "starwars"
        }))
        response = self.tester.post("/api/users",
                                    data=new_user_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_create_existing_user(self):
        """ 
            A test for creating an existing user
            The url endpoint is;
                =>    /api/users (post)
        """
        self.test_create_new_user()
        new_user_data = json.dumps(dict({
            "username" : "Juma",
            "first_name" : "Juma",
            "last_name" : "Mwangi",
            "email" : "juma@gmail.com",
            "password" : "starwars"
        }))
        response = self.tester.post("/api/users",
                                    data=new_user_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 409)
        self.assertIn("User already exists", str(response.data))

    def test_create_user_with_short_password(self):
        """ 
            A test for creating new users with a short password
            The url endpoint is;
                =>    /api/users (post)
        """
        new_user_data = json.dumps(dict({
            "username": "Sylvano",
            "email": "sylvano@gmail.com",
            "password": "war"
        }))
        response = self.tester.post("/api/users",
                                    data=new_user_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Incorrect credentials.", str(response.data))

    def test_create_user_with_bad_email(self):
        """ 
            A test for creating new users with a bad email
            The url endpoint is;
                =>    /api/users (post)
        """
        new_user_data = json.dumps(dict({
            "username" : "Jumai",
            "first_name" : "Jumai",
            "last_name" : "Mwangi",
            "email" : "jumai@gmail.com.com",
            "password" : "starwars"
        }))
        response = self.tester.post("/api/users",
                                    data=new_user_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Incorrect credentials.", str(response.data))

    def test_signin_non_existing_user(self):
        """ 
            A test for signing in non-existing user
            The url endpoint is;
                =>    /api/users/signin (post)
        """
        login_data = json.dumps(dict({
            "email": "nonexsting@gmail.com",
            "password": "nonexsting"
        }))
        response = self.tester.post("/api/users/signin",
                                    data=login_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_signout_user_with_auth(self):
        """ 
            A test for signing out user with authentication
            The url endpoint is;
                =>    /api/users/signout (get)
        """
        response = self.tester.get("/api/users/signout",
                                    headers=dict(Authorization='Bearer ' + self.token))
        self.assertEqual(response.status_code, 200)

    def test_signout_user_without_auth(self):
        """ 
            A test for signing out user without authentication
            The url endpoint is;
                =>    /api/users/signout (get)
        """
        response = self.tester.get("/api/users/signout")
        self.assertEqual(response.status_code, 403)

    def test_signout_user_with_invalid_auth(self):
        """ 
            A test for signing out user with invalid authentication
            The url endpoint is;
                =>    /api/users/signout (get)
        """
        response = self.tester.get("/api/users/signout",
                                    headers=dict(Authorization='Bearer' + self.token))
        self.assertEqual(response.status_code, 403)

    def test_signout_user_without_token(self):
        """ 
            A test for signing out user without a token
            The url endpoint is;
                =>    /api/users/signout (get)
        """
        response = self.tester.get("/api/users/signout",
                                    headers=dict(Authorization='Bearer'))
        self.assertEqual(response.status_code, 403)

    def test_signout_user_with_invalid_token(self):
        """ 
            A test for signing out user with invalid token
            The url endpoint is;
                =>    /api/users/signout (get)
        """
        response = self.tester.get("/api/users/signout",
                                    headers=dict(Authorization='Bearer SDSF@2.CDSFSfd.sAQedwsfe2w'))
        self.assertEqual(response.status_code, 401)

    def test_signout_with_banned_token(self):
        """ 
            A test for signing out user with a banned token
            The url endpoint is;
                =>    /api/users/signout (get)
        """
        self.test_signout_user_with_auth()
        response = self.tester.get("/api/users/signout",
                                    headers=dict(Authorization='Bearer ' + self.token))
        self.assertEqual(response.status_code, 401)
    
    def test_get_a_404_page(self):
        """
            A test to get a 404 page when the url does not exist
        """
        response = self.tester.get('/brew',
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_get_index_page(self):
        """
            A test to get the index page to see if it loads
        """
        response = self.tester.get('/',
                                    headers=dict(Authorization='Bearer ' + self.token), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
