from Mongo_class import Mongo_pizza
from Eaternity_class import Eaternity_class
from migros_class import MigrosAPI
from tqdm import tqdm

class Logic():

    def __init__(self):
        print("Loading...")
        self.pm = Mongo_pizza()
        self.ec = Eaternity_class()
        self.ma = MigrosAPI()
        self.user = "Peter"
        self.kitchen = "Kitchen_Peter"
        print("Server ready")

    def conver_ingredient(self, mongo_dict, migros_dict):
        """
        Join data fron ingredients
        """
        return {
                "id": mongo_dict['id'],
                "names": [{"language": "en", "value":mongo_dict['names']}],
                "amount": mongo_dict['amount'],
                "unit": mongo_dict['unit'],
                "origin": "Germany",
                "transport": "ground",
                "production": mongo_dict['production'],
                "conservation":mongo_dict['conservation']
        }

    def return_data(self, ingredients, location="Switzerland"):
        """
        Return data
            ingredients: list data
        """
        self.ec.create_kitchen(self.user, self.kitchen, location)
        aux = [self.pm.get_ingredient(i) for i in ingredients]
        aux = [self.conver_ingredient(i,[]) for i in aux]
        pizza_name = self.pm.classify_pizza(ingredients)
        aux = self.ec.put_recipe(pizza_name, self.kitchen,
                                 pizza_name, aux, location)
        for i in tqdm(ingredients):
            try:
                aux[i + " Nutritional"] = self.ma.get_nutritients(i)
            except IndexError:
                aux[i + " Nutritional"] = "None"

        return aux
