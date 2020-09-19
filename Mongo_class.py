import pymongo


class Mongo_pizza():

    def __init__(self, user="Peter", pwd="1234", table="Pizza_db"):
        client = pymongo.MongoClient(
                "mongodb+srv://" + user + ":" + pwd +
                "@cluster0.x2yjr.gcp.mongodb.net/" + table +
                "?retryWrites=true&w=majority")
        self.db = client.Pizza_db

    def classify_pizza(self, ingredients):
        """
        Classify Pizza
            ingredients: list of ingredients
        """
        for document in self.db.Pizza.find():
            for ingredient in ingredients:
                if ingredient in document["Key_ingredients"]:
                    return document["name"]
                    break
        return document["name"]

    def get_ingredient(self, ingredient_name):
        """
        Get ingredient element by name
            ingredient_name: string
        """
        aux =  list(self.db.Ingredient.find({"name":ingredient_name}))
        if len(aux) == 0:
            print("ERROR: Ingredient not found")
            return None
        return aux[0]

    def get_pizza(self, pizza_name):
        """
        Get ingredient element by name
            ingredient_name: string
        """
        aux =  list(self.db.Pizza.find({"name":pizza_name}))
        if len(aux) == 0:
            print("ERROR: Pizza not found")
            return None
        return aux[0]


    def insert_log(self, pizza_name, ingredients, co2):
        log = {"Pizza": pizza_name, "co2": co2}
        for ingredient in ingredients:
            name = ingredient["names"][0]['value']
            amount = ingredient["amount"]
            log[name] = amount
        self.db.Stats.insert_one(log)
