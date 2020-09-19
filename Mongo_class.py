import pymongo
import datetime

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
            self.pm.get_error("Error Mongo db, Ingredient not found ")
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
            self.pm.get_error("Error Mongo db, Pizza not found ")
            return None
        return aux[0]


    def insert_log(self, pizza_name, ingredients, co2, user, kitchen, co2=True):
        """
        Historical record from the query CO2
        """
        time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        log = {"Data": time, "Pizza": pizza_name, "co2": co2,
               "user": user, "Kitchen": kitchen}
        for ingredient in ingredients:
            name = ingredient["names"][0]['value']
            amount = ingredient["amount"]
            log[name] = amount
        self.db.Stats.insert_one(log)

    def get_error(self, error):
        """
        Historiacal record from the erros
        """
        print("Recording Error")
        time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        log = {"Data": time, "Error": error}
        self.db.Error_log.insert_one(log)
