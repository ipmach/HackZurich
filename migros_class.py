import requests
# from Mongo_class import Mongo_pizza

# mongodb = Mongo_pizza()

class MigrosAPI():

    def __init__(self):
        self.api = 'https://hackzurich-api.migros.ch/products'
        self.user = 'hackzurich2020'
        self.password = 'uhSyJ08KexKn4ZFS'
        self.headers = {
            'accept': 'application/json',
            'api-version': '7',
            'accept-language': 'de',
        }
        

    def get_nutritients(self, ingredient_name):
        """
        Nutritional facts
            ingredient_name: name of the ingredient
        """
        params = (
            ('search', ingredient_name),
            ('limit', '10'),
            ('offset', '0'),
            ('facet_sort_order', 'asc'),
            ('sort', 'score'),
            ('order', 'asc'),
            ('region', 'national'),
            ('view', 'browse'),
            ('verbosity', 'full'),
            ('custom_image', 'false'),
        )
        response = requests.get(self.api, 
            headers=self.headers, params=params, 
            auth=(self.user, self.password))

        response = response.json()
        # # nr. of products with given search key
        # n = response['total_hits']
        
        # just take first product
        return response['products'][0]['nutrition_facts']

"""
# function that maps from ingredient to location where it is from -> input for IBM CO2 database

def get_location(ingredient_name):
    params = (
        ('search', ingredient_name),
        ('limit', '10'),
        ('offset', '0'),
        ('facet_sort_order', 'asc'),
        ('sort', 'score'),
        ('order', 'asc'),
        ('region', 'national'),
        ('view', 'browse'),
        ('verbosity', 'full'),
        ('custom_image', 'false'),
    )
    response = requests.get('https://hackzurich-api.migros.ch/products', 
        headers=headers, params=params, auth=('hackzurich2020', 'uhSyJ08KexKn4ZFS'))

    response = response.json()
    # nr. of products with given search key
    n = response['total_hits']

    # nr. of products with given search key
    #filtered_response_list = response['products']
    
    # just take first product
    print(response['products'][0]['nutrition_facts'])
    print(response['products'][0].keys)
    print(response['products'][0]['origins'])
    product_origin = response['products'][0]['origins']['producing_country']
    print(product_origin)

    

    # # list of products with given search key
    # # print(response['products'][0].keys())
    # print(response['products'][0])
    # print(response['products'][0]['categories'])
    # # print(response['products'][0]['additional_categories'])
    return product_origin


# mongodb = 
get_location('Schinken')
"""