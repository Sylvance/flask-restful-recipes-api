import json
from tests.base_test_case import BaseTestCase

class CategoryTestCases(BaseTestCase):
    """
    Tests for the categories blueprint
    """
    def test_create_new_category(self):
        """
            A test for creating new categories
            The url endpoint is;
                =>    /api/users/user_id/categories (post)
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
        """
            A test for creating a category that already exists
            The url endpoint is;
                =>    /api/users/user_id/categories (post)
        """
        # Create an existing Category
        existing_category_data = json.dumps(dict({
            "title": "Kenyan",
            "description": "Dishes Made in Kenya"
        }))
        response = self.tester.post("/api/users/"+ str(self.user_id) +"/categories",
                                    data=existing_category_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 409)
        self.assertIn("Category already exists", str(response.data))

    def test_update_existing_category(self):
        """
            A test for updating categories
            The url endpoint is;
                =>    /api/users/{user_id}/categories/{category_id} (put)
        """
        # Update a Category
        new_category_data = json.dumps(dict({
            "title": "Chinese",
            "description": "Dishes Made in China"
        }))
        response = self.tester.put("/api/users/{}/categories/{}".format(self.user_id, self.category_id),
                                    data=new_category_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_update_category_with_existing_title(self):
        """
            A test for updating categories with a title that already exists
            The url endpoint is;
                =>    /api/users/{user_id}/categories/{category_id} (put)
        """
        # Update an existing Category
        existing_category_data = json.dumps(dict({
            "title": "Kenyan",
            "description": "Dishes Made in Kenya"
        }))
        response = self.tester.put("/api/users/{}/categories/{}".format(self.user_id, self.category_id),
                                    data=existing_category_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 409)
        self.assertIn("Category already exists", str(response.data))
    
    def test_get_category_by_id(self):
        """
            A test for getting categories by id
            The url endpoint is;
                =>    /api/users/id/categories/id (get)
        """
        response = self.tester.get("/api/users/{}/categories/{}".format(self.user_id, self.category_id),
                                    headers=dict(Authorization='Bearer ' + self.token))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Dishes Made in Kenya", str(response.data))
    
    def test_get_categories(self):
        """
            A test for getting categories
            The url endpoint is;
                =>    /api/users/id/categories (get)
        """
        response = self.tester.get("/api/users/{}/categories".format(self.user_id),
                                    headers=dict(Authorization='Bearer ' + self.token))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Dishes Made in Kenya", str(response.data))
    
    def test_delete_category_by_id(self):
        """
            A test for deleting categories by id
            The url endpoint is;
                =>    /api/users/id/categories/id (get)
        """
        response = self.tester.delete("/api/users/{}/categories/{}".format(self.user_id, self.category_id),
                                    headers=dict(Authorization='Bearer ' + self.token))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Delete", str(response.data))

if __name__ == "__main__":
    unittest.main()
