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
                "names": [{"language": "en", "value": mongo_dict['name']}],
                "amount": mongo_dict['amount'],
                "unit": mongo_dict['unit'],
                "origin": "Germany",
                "transport": "ground",
                "production": mongo_dict['production'],
                "conservation":mongo_dict['conservation']
        }

    def return_data_CO2(self, pizza_name, location="Switzerland"):
        """
        Return CO2 data
            pizza_name: string data
        """
        a = self.ec.create_kitchen(self.user, self.kitchen, location)
        if a[1]:
            self.pm.get_error(a[0])
        ingredients = self.pm.get_pizza(pizza_name)['Ingredients']
        aux_ingr = [self.pm.get_ingredient(i) for i in ingredients]
        aux = [self.conver_ingredient(i,[]) for i in aux_ingr]
        aux, a = self.ec.put_recipe("Recipe", self.kitchen,
                                 "Recipe", aux, location)
        if a:
            self.pm.get_error(aux)
            raise Exception
        self.pm.insert_log(pizza_name,
                           ingredients,
                           aux['recipe']['co2-value'],
                           self.user, self.kitchen, "Return co2")
        return aux

    def return_data_pizza(self, pizza_name, location="Switzerland"):
        """
        Return ingredients from pizza
            pizza_name: string data
        """
        self.ec.create_kitchen(self.user, self.kitchen, location)
        ingredients = self.pm.get_pizza(pizza_name)['Ingredients']
        self.pm.insert_log(pizza_name,
                           ingredients,
                           -1,
                           self.user, self.kitchen, "Return ingredients")
        return {"ingredients": ingredients}
