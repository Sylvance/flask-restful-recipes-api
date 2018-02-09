"""The tests for the app"""
import sys, os
import unittest
import flask
import json
import jwt


path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path + '/../')

from code import create_app, db
from flask import current_app

class BaseTestCase(unittest.TestCase):
    """Base test case class."""
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

        # Create a Recipe
        recipe_data = json.dumps(dict({
            "category_id" : self.category_id,
            "title" : "uji",
            "description" : "white"
        }))
        response = self.tester.post("/api/categories/"+ str(self.category_id) +"/recipes",
                                    data=recipe_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json")
        res = json.loads(response.data.decode())
        self.recipe_id = res['id']

if __name__ == "__main__":
    unittest.main()
