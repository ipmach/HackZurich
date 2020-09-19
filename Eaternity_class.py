import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

class Eaternity_class():

    def __init__(self, key="SR001CHbX2t3wv0oFpA6TPWjrOUmILzR"):
        self.AUTH = HTTPBasicAuth(key, "")
        self.BASE_URL = "https://co2.eaternity.ch"

    def create_kitchen(self, name, kitchen_id, location):
        """
        Initialize a kitchen
            name: name user
            kitchen_id: id kitchen
            location: location kitchen
        """
        url = "{}/api/kitchens/{}".format(self.BASE_URL, kitchen_id)

        body = {
            "kitchen": {
                "name": name,
                "location": location
            }
        }

        response = requests.put(url, json=body, auth=self.AUTH)
        if response.status_code not in [200, 201, 202]:
            print(f"ERROR: Failed PUTting kitchen {kitchen_id}" +
                  f" with status {response.status_code}: '{response.text}'")
        else:
            print(f"SUCCESS: PUT kitchen {kitchen_id}")
            return response.json()

    def put_recipe(self, recipe_id, kitchen_id,
                   name_pizza, list_ingredientes, location):
        """
        Insert a recipe to optain info like co2
            recipe_id: id recipe
            kitchen_id: kitchen id
            name_pizza: pizza id
            list_ingredientes: list of ingredients
            location: location of kitchens
        """
        url = "{}/api/kitchens/{}/recipes/{}".format(self.BASE_URL,
                                                     kitchen_id, recipe_id)

        body = {
            "recipe": {
                "titles": [
                    {
                        "language": "en",
                        "value": name_pizza
                    }
                ],
                "date": datetime.now().strftime("%Y-%m-%d"),
                "location": location,
                "servings": 1,
                "ingredients": list_ingredientes
            }
        }
        response = requests.put(url, json=body, auth=self.AUTH)
        if response.status_code not in [200, 201, 202]:
            print(f"ERROR: Failed PUTting recipe {recipe_id} with" +
                  f" status {response.status_code}: '{response.text}'")
        else:
            print(f"SUCCESS: PUT recipe {recipe_id}")
            response = response.json()
            response['recipe']['ingredients'] = list_ingredientes
            return response
