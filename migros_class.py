import requests
from difflib import SequenceMatcher
from heapq import nlargest as _nlargest


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

    def get_nutrients(self, ingredient_name):
        """
        Retrieve nutritional facts
            ingredient_name: name of the ingredient
        """
        params = (
            ('search', ingredient_name),
            ('facets[category][]', 'BeSS_0101'),
            ('limit', '100'),
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

        # find matching product and return corresponding nutrients
        matching_product = self.get_best_fit(response, ingredient_name)
        nutrients = self.beautify_nutrients(matching_product['nutrition_facts'])

        return nutrients

    def get_location(self, ingredient_name):
        """
        Retrieve location of ingredient
            ingredient_name: name of the ingredient
        """
        params = (
            ('search', ingredient_name),
            ('facets[category][]', 'BeSS_0101'),
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

        matching_product = self.get_best_fit(response, ingredient_name)

        return matching_product['origins']['producing_country']

    def get_price(self, ingredient_name):
        """
        Retrieve price of ingredient
            ingredient_name: name of the ingredient
        """
        params = (
            ('search', ingredient_name),
            ('facets[category][]', 'BeSS_0101'),
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

        matching_product = self.get_best_fit(response, ingredient_name)

        return matching_product['price']

    def get_best_fit(self, products_json, ingredient_name):
        """
        Get best fitting product to search query
            products_json: json as retrieved from the migros API query
            ingredient_name: name for which we search the product catalogue
        """
        # get list of names
        product_names = []
        for i in range(len(products_json['products'])):
            product_names.append(products_json['products'][i]['name'])

        # get index of result with closest match
        best_fit_index = self.get_best_fit_index(ingredient_name,
                            product_names, 1)

        return products_json['products'][best_fit_index[0]]

    def get_best_fit_index(self, word, possibilities, n=1, cutoff=0):
        """ Source: https://stackoverflow.com/questions/50861237/is-there-an-alternative-to-difflib-get-close-matches-that-returns-indexes-l
        Use SequenceMatcher to return a list of the indexes of the best
        "good enough" matches. word is a sequence for which close matches
        are desired (typically a string).
        possibilities is a list of sequences against which to match word
        (typically a list of strings).
        Optional arg n (default 3) is the maximum number of close matches to
        return.  n must be > 0.
        Optional arg cutoff (default 0.6) is a float in [0, 1].  Possibilities
        that don't score at least that similar to word are ignored.
        """
        if not n >  0:
            raise ValueError("n must be > 0: %r" % (n,))
        if not 0.0 <= cutoff <= 1.0:
            raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))
        result = []
        s = SequenceMatcher()
        s.set_seq2(word)
        for idx, x in enumerate(possibilities):
            s.set_seq1(x)
            if s.real_quick_ratio() >= cutoff and \
               s.quick_ratio() >= cutoff and \
               s.ratio() >= cutoff:
                result.append((s.ratio(), idx))

        # Move the best scorers to head of list
        result = _nlargest(n, result)

        # Strip scores for the best n matches
        return [x for score, x in result]


    def beautify_nutrients(self, nutrition_facts):
        """
        Brings the nutritional facts of the product to desired form
            nutritional_facts: JSON of the nutrients
        """
        # set up first column
        nutrition_facts = nutrition_facts['standard']

        nutrients = {}
        nutrients['Quantity'] = [nutrition_facts['base_quantity'],
                                nutrition_facts['base_unit']]

        # loop over all columns in nutrition_facts and build dict
        for i in range(len(nutrition_facts['nutrients'])):
            nutrients[nutrition_facts['nutrients'][i]['name']] = [
                    nutrition_facts['nutrients'][i]['quantity'],
                    nutrition_facts['nutrients'][i]['quantity_unit'],

                ]

        return nutrients
