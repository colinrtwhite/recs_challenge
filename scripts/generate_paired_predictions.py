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

with open('given/item_to_item_collaborative_similarity.json', 'rb') as f:
    product_similarity = json.load(f)

with open('given/category_similarity.json', 'rb') as f:
    category_similarity = json.load(f)

with open('given/sub_category_similarity.json', 'rb') as f:
    sub_category_similarity = json.load(f)

with open('given/brand_similarity.json', 'rb') as f:
    brand_similarity = json.load(f)

with open('given/price_range_similarity.json', 'rb') as f:
    price_range_similarity = json.load(f)

product_consistency = {}
max_consistency = 0
with open('given/product_consistency.json', 'rb') as f:
    consistency_json = json.load(f)
    for item in consistency_json:
        product_consistency[item[0]] = log(item[1])
        max_consistency = max(max_consistency, product_consistency[item[0]])


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
                    if related_product is not product:
                        related_product_attributes = product_to_attributes[related_product]
                        # MOST IMPORTANT LINE IN THIS WHOLE ALGORITHM: HOW AND WHAT WE WEIGHT
                        weighted_related_products.append((related_product, product_similarity[product][related_product]))

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
