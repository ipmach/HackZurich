from Mongo_class import Mongo_pizza
from Eaternity_class import Eaternity_class


pm = Mongo_pizza()
ec = Eaternity_class()


def conver_ingredient(mongo_dict, migros_dict):
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

location = "Switzerland"

ec.create_kitchen("Peter", "Kitchen_Peter", "Switzerland")

a = [pm.get_ingredient("Pineapple"), pm.get_ingredient("Corn")]

a = [conver_ingredient(i,[]) for i in a]

print(ec.put_recipe("Margarita", "Kitchen_Peter", "Margarita", a, "Switzerland"))
