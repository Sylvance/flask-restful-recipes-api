import json
from tests.base_test_case import BaseTestCase

class RecipeTestCases(BaseTestCase):
    """
    Tests for the recipes blueprint
    """
    def test_create_new_recipe(self):
        """
            A test for creating new recipes
            The url endpoint is;
                =>    /api/categories/id/recipes (post)
        """
        # Create a Recipe
        new_recipe_data = json.dumps(dict({
            "category_id" : self.category_id,
            "title" : "porridge",
            "description" : "brown"
        }))
        response = self.tester.post("/api/categories/"+str(self.category_id)+"/recipes",
                                    data=new_recipe_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_create_existing_recipe(self):
        """
            A test for creating existing recipes
            The url endpoint is;
                =>    /api/categories/id/recipes (post)
        """
        # Create a Recipe
        new_recipe_data = json.dumps(dict({
            "category_id" : self.category_id,
            "title" : "uji",
            "description" : "white"
        }))
        response = self.tester.post("/api/categories/"+str(self.category_id)+"/recipes",
                                    data=new_recipe_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 409)
    
    def test_update_recipe_by_id(self):
        """
            A test for updating recipes by id
            The url endpoint is;
                =>    /api/categories/id/recipes/id (put)
        """
        # Create a Recipe
        new_recipe_data = json.dumps(dict({
            "category_id" : self.category_id,
            "title" : "porridge",
            "description" : "brown"
        }))
        response = self.tester.put("/api/categories/"+str(self.category_id)+"/recipes/{}".format(self.recipe_id),
                                    data=new_recipe_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_update_recipe_with_existing_title(self):
        """
            A test for updating recipes existing title
            The url endpoint is;
                =>    /api/categories/id/recipes/id (put)
        """
        # Create a Recipe
        new_recipe_data = json.dumps(dict({
            "category_id" : self.category_id,
            "title" : "uji",
            "description" : "white"
        }))
        response = self.tester.put("/api/categories/"+str(self.category_id)+"/recipes/{}".format(self.recipe_id),
                                    data=new_recipe_data,
                                    headers=dict(Authorization='Bearer ' + self.token),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 409)
    
    def test_get_recipes(self):
        """
            A test for listing all recipes
            The url endpoint is;
                =>    /api/categories/id/recipes (get)
        """
        response = self.tester.get("/api/categories/"+str(self.category_id)+"/recipes",
                                    headers=dict(Authorization='Bearer ' + self.token))
        self.assertEqual(response.status_code, 200)

    def test_get_recipe_by_id(self):
        """
            A test for listing a recipe
            The url endpoint is;
                =>    /api/categories/id/recipes/id (get)
        """
        response = self.tester.get("/api/categories/"+str(self.category_id)+"/recipes/{}".format(self.recipe_id),
                                    headers=dict(Authorization='Bearer ' + self.token))
        self.assertEqual(response.status_code, 200)

    def test_delete_recipe_by_id(self):
        """
            A test for deleting recipes
            The url endpoint is;
                =>    /api/categories/id/recipes/id (delete)
        """
        response = self.tester.delete("/api/categories/"+str(self.category_id)+"/recipes/{}".format(self.recipe_id),
                                    headers=dict(Authorization='Bearer ' + self.token))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Delete", str(response.data))

if __name__ == "__main__":
    unittest.main()
