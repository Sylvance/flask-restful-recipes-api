""" The tests for the app"""
import sys, os
import unittest
import flask
import json
import jwt


path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path + '/../')

from code import create_app, db
from flask import current_app

class AuthTestCases(unittest.TestCase):
    """
    Tests for the authentication blueprint
    """
    def setUp(self):
        """
        Sets up the application for tests
        """
        # Application setup
        self.app = create_app()

        # Database setup
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

        # Test client
        self.tester = self.app.test_client()

        # Create a User
        self.user_data = json.dumps(dict({
            "username" : "Jumai",
            "first_name" : "Jumai",
            "last_name" : "Mwangi",
            "email" : "jumai@gmail.com",
            "password" : "starwars"
        }))
        response = self.tester.post("/api/users",
                                    data=self.user_data,
                                    content_type="application/json")
        
        # Sign in user
        self.login_data = json.dumps(dict({
            "email" : "jumai@gmail.com",
            "password" : "starwars"
        }))
        response = self.tester.post("/api/users/signin",
                                    data=self.login_data,
                                    content_type="application/json")
        res = json.loads(response.data.decode())
        self.token = res['token']
        payload = jwt.decode(self.token, 
                             'xoi82SJuX98#*$aIAjakj3sus',
                             algorithms='HS256')
        self.user_id = payload['sub']
    
    def test_get_users(self):
        """ 
            A test for retrieving list of users
            The url endpoint is;
                =>    /users (get)
        """
        response = self.tester.get('/api/users',
                                    headers=dict(Authorization='Bearer ' + self.token), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_create_new_user(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
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
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
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

    def test_create_user_with_bad_password(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        new_user_data = json.dumps(dict({
            "username": "Sylvano",
            "email": "sylvano@gmail.com",
            "password": "war"
        }))
        response = self.tester.post("/api/users",
                                    data=new_user_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("Incorrect credentials. Email should be correct. \
                        Password should be more than 6 characters", str(response.data))

    def test_create_user_with_bad_email(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
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
        self.assertEqual(response.status_code, 401)
        self.assertIn("Incorrect credentials. Email should be correct. \
                        Password should be more than 6 characters", str(response.data))

    def test_signin_non_existing_user(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        login_data = json.dumps(dict({
            "email": "nonexsting@gmail.com",
            "password": "nonexsting"
        }))
        response = self.tester.post("/api/users/signin",
                                    data=login_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_signin_non_wrong_email(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        login_data = json.dumps(dict({
            "email": "nonexsting.com",
            "password": "nonexsting"
        }))
        response = self.tester.post("/api/users/signin",
                                    data=login_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_signout_user_with_auth(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        response = self.tester.post("/api/users/signout",
                                    headers=dict(Authorization='Bearer ' + self.token))
        self.assertEqual(response.status_code, 403)

    def test_signout_user_without_auth(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        response = self.tester.post("/api/users/signout")
        self.assertEqual(response.status_code, 403)

    def test_signout_user_with_invalid_auth(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        response = self.tester.post("/api/users/signout",
                                    headers=dict(Authorization='Bearer' + self.token))
        self.assertEqual(response.status_code, 403)

    def test_signout_user_with_invalid_token(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        response = self.tester.post("/api/users/signout",
                                    headers=dict(Authorization='Bearer'))
        self.assertEqual(response.status_code, 403)

    def test_signout_user_with_incorrect_token(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        response = self.tester.post("/api/users/signout",
                                    headers=dict(Authorization='Bearer SDSF@2.CDSFSfd.sAQedwsfe2w'))
        self.assertEqual(response.status_code, 401)

    def test_signin_with_banned_token(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        self.test_signout_user_with_auth()
        response = self.tester.post("/api/users/signout",
                                    headers=dict(Authorization='Bearer' + self.token))
        self.assertEqual(response.status_code, 403)
    
    def test_get_404(self):
        """ 
        """
        response = self.tester.get('/brew',
                                    headers=dict(Authorization='Bearer ' + self.token), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_get_index(self):
        """ 
        """
        response = self.tester.get('/',
                                    headers=dict(Authorization='Bearer ' + self.token), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
