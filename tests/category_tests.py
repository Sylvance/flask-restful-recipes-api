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

        # Create a Category
        self.category_data = json.dumps(dict({
            "title": "Kenyan",
            "description": "Dishes Made in Kenya"
        }))
        response = self.tester.post("/api/users/"+ str(self.user_id) +"/categories",
                                    data=self.category_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json")
        res = json.loads(response.data.decode())
        self.category_id = res['id']

    
    # def test_get_categories(self):
    #     """ 
    #         A test for retrieving list of categories
    #         The url endpoint is;
    #             =>    /categories (get)
    #     """
    #     response = self.tester.post("/api/users/"+ str(self.user_id) +"/categories",
    #                                 headers=dict(Authorization='Bearer ' + self.token),
    #                                 content_type="application/json")
    #     print(response.data)
    #     self.assertEqual(response.status_code, 201)

    def test_create_new_category(self):
        """ 
            A test for creating new categories
            The url endpoint is;
                =>    /categories (post)
        """
        # Create a Category
        new_category_data = json.dumps(dict({
            "title": "Chinese",
            "description": "Dishes Made in China"
        }))
        response = self.tester.post("/api/users/"+ str(self.user_id) +"/categories",
                                    data=new_category_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_create_existing_category(self):
        existing_category_data = json.dumps(dict({
            "title": "Kenyan",
            "description": "Dishes Made in Kenya"
        }))
        response = self.tester.post("/api/users/"+ str(self.user_id) +"/categories",
                                    data=existing_category_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json") 
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()