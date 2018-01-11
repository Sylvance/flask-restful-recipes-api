""" The tests for the app"""
import os
import unittest
import flask
import json
import jwt

from app import create_app, db
from flask import current_app as app
from common.config import app_config


class BasicTestCase(unittest.TestCase):
    """
    These are tests for the url enpoints for the app.
       The url endpoints are;
          1.  /users         (get)  GET all users
          2.  /users         (post) CREATE new user
          3.  /categories    (get)  GET all categories
          4.  /categories    (post) CREATE new category
          5.  /recipes       (get)  GET all recipes
          6.  /recipes       (post) CREATE new recipe
          7.  /user/:id      (get)  GET single user
          8.  /category/:id  (get)  GET single category
          9.  /recipe/:id    (get)  GET single recipe
          10. /user/:id      (put)  PUT single user
          11. /category/:id  (put)  PUT single category
          12. /recipe/:id    (put)  PUT single recipe
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
            "username": "Sylvance",
            "email": "ksylvance@gmail.com",
            "bio": "I am good",
            "password": "waroftitans"
        }))
        response = self.tester.post("/api/v1/signup",
                                    data=self.user_data,
                                    content_type="application/json")
        
        # Sign in user
        self.login_data = json.dumps(dict({
            "email": "ksylvance@gmail.com",
            "password": "waroftitans"
        }))
        response = self.tester.post("/api/v1/signin",
                                    data=self.login_data,
                                    content_type="application/json")
        res = json.loads(response.data.decode())
        self.token = res['auth_token']
        payload = jwt.decode(self.token, 
                             app_config['testing'].SECRET_KEY,
                             algorithms='HS256')
        self.user_id = payload['sub']

        # Create a Category
        self.category_data = json.dumps(dict({
            "categorytitle": "Kenyan Dishes",
            "categorydescription": "Dishes Made in Kenya",
            "user_id": self.user_id
        }))
        response = self.tester.post("/api/v1/categories",
                                    data=self.category_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json")
        res = json.loads(response.data.decode())
        self.category_id = res['id']

        # Create a Recipe
        recipe_data = json.dumps(dict({
            "recipetitle": "Chapati",
            "recipedescription": "Round, brown and good",
            "category_id": self.category_id
        }))
        response = self.tester.post("/api/v1/recipes",
                                    data=recipe_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json")
        res = json.loads(response.data.decode())
        self.recipe_id = res['id']

    def test_get_users(self):
        """ 
            A test for retrieving list of users
            The url endpoint is;
                =>    /users (get)
        """
        response = self.tester.get('/api/v1/users',
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
            "username": "Sylvano",
            "email": "sylvano@gmail.com",
            "bio": "I am good",
            "password": "waroftitans"
        }))
        response = self.tester.post("/api/v1/signup",
                                    data=new_user_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_reset_password(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        new_password = json.dumps(dict({
            "password": "waroftitans1234"
        }))
        response = self.tester.put("/api/v1/resetpassword/user/{}".
                                   format(self.user_id),
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   data=new_password,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_create_existing_user(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        self.test_create_new_user()
        new_user_data = json.dumps(dict({
            "username": "Sylvano",
            "email": "sylvano@gmail.com",
            "bio": "I am good",
            "password": "waroftitans"
        }))
        response = self.tester.post("/api/v1/signup",
                                    data=new_user_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_create_user_with_bad_password(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        new_user_data = json.dumps(dict({
            "username": "Sylvano",
            "email": "sylvano@gmail.com",
            "bio": "I am good",
            "password": "war"
        }))
        response = self.tester.post("/api/v1/signup",
                                    data=new_user_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_create_user_with_bad_email(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        new_user_data = json.dumps(dict({
            "username": "Sylvano",
            "email": "sylvano@",
            "bio": "I am good",
            "password": "waroftitans"
        }))
        response = self.tester.post("/api/v1/signup",
                                    data=new_user_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

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
        response = self.tester.post("/api/v1/signin",
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
        response = self.tester.post("/api/v1/signin",
                                    data=login_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_signout_user_with_auth(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        response = self.tester.post("/api/v1/signout",
                                    headers=dict(Authorization='Bearer ' + self.token))
        self.assertEqual(response.status_code, 200)

    def test_signout_user_without_auth(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        response = self.tester.post("/api/v1/signout")
        self.assertEqual(response.status_code, 403)

    def test_signout_user_with_invalid_auth(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        response = self.tester.post("/api/v1/signout",
                                    headers=dict(Authorization='Bearer' + self.token))
        self.assertEqual(response.status_code, 403)

    def test_signout_user_with_invalid_token(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        response = self.tester.post("/api/v1/signout",
                                    headers=dict(Authorization='Bearer'))
        self.assertEqual(response.status_code, 403)

    def test_signout_user_with_incorrect_token(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        response = self.tester.post("/api/v1/signout",
                                    headers=dict(Authorization='Bearer SDSF@2.CDSFSfd.sAQedwsfe2w'))
        self.assertEqual(response.status_code, 401)

    def test_signin_with_banned_token(self):
        """ 
            A test for creating new users
            The url endpoint is;
                =>    /users (post)
        """
        self.test_signout_user_with_auth()
        response = self.tester.post("/api/v1/signout",
                                    headers=dict(Authorization='Bearer' + self.token))
        self.assertEqual(response.status_code, 403)

    def test_get_categories(self):
        """ 
            A test for retrieving list of categories
            The url endpoint is;
                =>    /categories (get)
        """
        response = self.tester.get('/api/v1/categories',
                                    headers=dict(Authorization='Bearer ' + self.token), 
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_create_new_category(self):
        """ 
            A test for creating new categories
            The url endpoint is;
                =>    /categories (post)
        """
        # Create a Category
        user_id = self.user_id
        new_category_data = json.dumps(dict({
            "categorytitle": "Chinese Dishes",
            "categorydescription": "Dishes Made in China",
            "user_id": user_id
        }))
        response = self.tester.post("/api/v1/categories",
                                    data=new_category_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_create_existing_category(self):
        existing_category_data = json.dumps(dict({
            "categorytitle": "Kenyan Dishes",
            "categorydescription": "Dishes Made in Kenya",
            "user_id": self.user_id
        }))
        response = self.tester.post("/api/v1/categories",
                                    data=existing_category_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json") 
        self.assertEqual(response.status_code, 200)       

    def test_get_recipes(self):
        """ 
            A test for retrieving list of recipes
            The url endpoint is;
                =>    /recipes (get)
        """
        response = self.tester.get('/api/v1/recipes',
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_create_new_recipe(self):
        """ 
            A test for creating new recipes
            The url endpoint is;
                =>    /recipes (post)
        """
        # Create a Recipe
        category_id = self.category_id
        new_recipe_data = json.dumps(dict({
            "recipetitle": "Rice and Beans",
            "recipedescription": "White, brown and sweet",
            "category_id": category_id
        }))
        response = self.tester.post("/api/v1/recipes",
                                    data=new_recipe_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_single_user(self):
        """ 
            A test for retrieving singe user
            The url endpoint is;
                =>    /user/:id (get)
        """
        response = self.tester.get('/api/v1/user/{}'.
                                   format(self.user_id),
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_single_category(self):
        """ 
            A test for retrieving singe category
            The url endpoint is;
                =>    /category/:id (get)
        """
        response = self.tester.get('/api/v1/category/{}'.
                                   format(self.category_id),
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_single_recipe(self):
        """ 
            A test for retrieving singe recipe
            The url endpoint is;
                =>    /recipe/:id (get)
        """
        response = self.tester.get('/api/v1/recipe/{}'.
                                   format(self.recipe_id),
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_single_user(self):
        """ 
            A test for updating singe user
            The url endpoint is;
                =>    /user/:id (put)
        """
        # Put a User
        put_user_data = json.dumps(dict({
            "username": "Sylvanco",
            "email": "sylvance@gmail.com",
            "bio": "I am good"
        }))
        response = self.tester.put('/api/v1/user/{}'.
                                   format(self.user_id),
                                   data=put_user_data,
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_single_user_bio(self):
        """ 
            A test for updating singe user
            The url endpoint is;
                =>    /user/:id (put)
        """
        # Put a User
        put_user_data = json.dumps(dict({
            "bio": "I am good"
        }))
        response = self.tester.put('/api/v1/updatebio/user/{}'.
                                   format(self.user_id),
                                   data=put_user_data,
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_single_user_email(self):
        """ 
            A test for updating singe user
            The url endpoint is;
                =>    /user/:id (put)
        """
        # Put a User
        put_user_data = json.dumps(dict({
            "email": "sylvance@gmail.com"
        }))
        response = self.tester.put('/api/v1/updateemail/user/{}'.
                                   format(self.user_id),
                                   data=put_user_data,
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_single_category(self):
        """ 
            A test for updating singe category
            The url endpoint is;
                =>    /category/:id (put)
        """
        # Put a Category
        put_category_data = json.dumps(dict({
            "categorytitle": "Kenyan Dishes reloaded",
            "categorydescription": "Dishes Made in Kenyan soil"
        }))
        response = self.tester.put("/api/v1/category/{}".
                                   format(self.category_id),
                                   data=put_category_data,
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_put_single_category_title(self):
        """ 
            A test for updating singe category
            The url endpoint is;
                =>    /category/:id (put)
        """
        # Put a Category
        put_category_data = json.dumps(dict({
            "categorytitle": "Kenyan Dishes reloaded"
        }))
        response = self.tester.put("/api/v1/updatetitle/category/{}".
                                   format(self.category_id),
                                   data=put_category_data,
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_put_single_category_description(self):
        """ 
            A test for updating singe category
            The url endpoint is;
                =>    /category/:id (put)
        """
        # Put a Category
        put_category_data = json.dumps(dict({
            "categorydescription": "Dishes Made in Kenyan soil"
        }))
        response = self.tester.put("/api/v1/updatedescription/category/{}".
                                   format(self.category_id),
                                   data=put_category_data,
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_put_single_recipe(self):
        """ 
            A test for updating singe recipe
            The url endpoint is;
                =>    /recipe/:id (put)
        """
        # Update a Recipe
        put_recipe_data = json.dumps(dict({
            "recipetitle": "Chapati reloaded",
            "recipedescription": "Round, brown and sweet",
            "category_id": self.category_id
        }))
        response = self.tester.put('/api/v1/recipe/{}'.
                                   format(self.recipe_id),
                                   data=put_recipe_data,
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_single_recipe_title(self):
        """ 
            A test for updating singe recipe
            The url endpoint is;
                =>    /recipe/:id (put)
        """
        # Update a Recipe
        put_recipe_data = json.dumps(dict({
            "recipetitle": "Chapati reloaded"
        }))
        response = self.tester.put('/api/v1/updatetitle/recipe/{}'.
                                   format(self.recipe_id),
                                   data=put_recipe_data,
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_single_recipe_description(self):
        """ 
            A test for updating singe recipe
            The url endpoint is;
                =>    /recipe/:id (put)
        """
        # Update a Recipe
        put_recipe_data = json.dumps(dict({
            "recipedescription": "Round, brown and sweet"
        }))
        response = self.tester.put('api/v1/updatedescription/recipe/{}'.
                                   format(self.recipe_id),
                                   data=put_recipe_data,
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_single_user(self):
        """ 
            A test for retrieving singe user
            The url endpoint is;
                =>    /user/:id (delete)
        """
        response = self.tester.delete('/api/v1/user/{}'.
                                   format(self.user_id),
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_delete_single_category(self):
        """ 
            A test for retrieving singe category
            The url endpoint is;
                =>    /category/:id (delete)
        """
        response = self.tester.delete('/api/v1/category/{}'.
                                   format(self.category_id),
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_delete_single_recipe(self):
        """ 
            A test for retrieving singe recipe
            The url endpoint is;
                =>    /recipe/:id (delete)
        """
        response = self.tester.delete('/api/v1/recipe/{}'.
                                   format(self.recipe_id),
                                   headers=dict(Authorization='Bearer ' + self.token),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
