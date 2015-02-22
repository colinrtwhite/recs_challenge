#!/usr/bin/python

import operator
import json
from math import log

# Generates a set of predictions for each customer, based on products which we know to be connected to those in their
# purchase history.

customer_purchases = {}
with open('data/customer_products.csv', 'rb') as f:
    for line in f:
        values = line.strip().split(',')
        customer_purchases[values[0]] = values[1:]

with open('given/product_to_attributes.json', 'rb') as f:
    product_to_attributes = json.load(f)

with open('given/product_similarity.json', 'rb') as f:
    product_similarity = json.load(f)

with open('given/category_similarity.json', 'rb') as f:
    category_similarity = json.load(f)

with open('given/sub_category_similarity.json', 'rb') as f:
    sub_category_similarity = json.load(f)

with open('given/brand_similarity.json', 'rb') as f:
    brand_similarity = json.load(f)

with open('given/price_range_similarity.json', 'rb') as f:
    price_range_similarity = json.load(f)

with open('given/product_consistency_normalised.json', 'rb') as f:
    product_consistency = json.load(f)

# WEIGHTS (please keep them added up to 1.0)
PRODUCT_WEIGHT = 0.45
CATEGORY_WEIGHT = 0.1
SUB_CATEGORY_WEIGHT = 0.1
BRAND_WEIGHT = 0.1
PRICE_RANGE_WEIGHT = 0.1
PRODUCT_CONSISTENCY_WEIGHT = 0.15

weighted_related_products_for_product = {}
customer_paired_predictions = {}
for customer in customer_purchases:
    customer_paired_products = []

    for product in customer_purchases[customer]:
        if product in product_similarity:
            # MODIFICATION: USED weighted_related_products_for_product TO CACHE RESULT PER PRODUCT
            if product not in weighted_related_products_for_product:
                product_attributes = product_to_attributes[product]
                weighted_related_products = []
                for related_product in product_similarity[product]:
                    related_product_attributes = product_to_attributes[related_product]
                    # MOST IMPORTANT LINE IN THIS WHOLE ALGORITHM: HOW AND WHAT WE WEIGHT
                    weighted_related_products.append((related_product, PRODUCT_WEIGHT * product_similarity[product][related_product] +
                                                      CATEGORY_WEIGHT * category_similarity[product_attributes['category']][related_product_attributes['category']] +
                                                      SUB_CATEGORY_WEIGHT * sub_category_similarity[product_attributes['sub_category']][related_product_attributes['sub_category']] +
                                                      BRAND_WEIGHT * brand_similarity[product_attributes['brand']][related_product_attributes['brand']] +
                                                      PRICE_RANGE_WEIGHT * price_range_similarity[product_attributes['price_range']][related_product_attributes['price_range']] +
                                                      PRODUCT_CONSISTENCY_WEIGHT * product_consistency[related_product]))

                weighted_related_products_for_product[product] = weighted_related_products

            customer_paired_products += weighted_related_products_for_product[product]
            # MODIFICATION

    paired_predictions = sorted(customer_paired_products, key=operator.itemgetter(1), reverse=True)[:6]

    customer_paired_predictions[customer] = paired_predictions

# ADRIAN: SEPARATED DATA EXPORT FROM ABOVE TO BELLOW
with open('data/customer_paired_predictions.csv', 'w+') as f:
    for customer_id, paired_predictions in customer_paired_predictions.items():
        f.write(customer_id)
        for rec_product in paired_predictions:
            f.write(',%s:%s' % (rec_product[0], str(rec_product[1])))
        f.write('\n')
