#!/usr/bin/python

import operator
import json

# Generates a set of predictions for each customer, based on products which we know to be connected to those in their
# purchase history

customer_purchases = {}
with open('data/customer_products.csv', 'rb') as f:
    for line in f:
        values = line.strip().split(',')
        customer_purchases[values[0]] = values[1:]

product_pairs = {}
with open('data/paired_products.csv', 'rb') as f:
    for line in f:
        values = line.strip().split(',')
        product_pairs[values[0]] = map(lambda s : (s.split(':')[0], float(s.split(':')[1])), values[1:])

product_consistency = {}
with open('given/product_consistency.json', 'rb') as f:
    j = json.load(f)
    for item in j:
        product_consistency[item[0]] = item[1]

# Not 100% sure what is going on in here.
# Output is in the form of:
# customer_id, (paired_product_id : total_pair_value)*6
# total_pair_value is the sum of all pair frequencies for the items in customer_id's order history with respect to
# paired_product_id
# NOTE: The (paired_product_id:...) is sorted descending by its "total pair value". Also, I believe its total pair value
# accounts for multiples in order history.

weighted_related_products_for_product = {}
customer_paired_predictions = {}
index = 0

for customer in customer_purchases:
    customer_paired_products = []

    for product in customer_purchases[customer]:
        if product in product_pairs:
            # MODIFICATION

            #ADRIAN: USED weighted_related_products_for_product TO CACHE RESULT PER PRODUCT
            if product not in weighted_related_products_for_product:

                weighted_related_products = []
                for related_product in product_pairs[product]:
                    weighted_related_products.append((related_product[0], 0.9 * related_product[1] + 0.05 * product_consistency[related_product[0]]))

                weighted_related_products_for_product[product] = weighted_related_products

            # MODIFICATION
            customer_paired_products += weighted_related_products_for_product[product]

    paired_predictions = sorted(customer_paired_products, key = operator.itemgetter(1), reverse = True)[:6]

    customer_paired_predictions[customer] = paired_predictions

# ADRIAN: SEPARATED DATA EXPORT FROM ABOVE TO BELLOW
index = 0
with open('data/customer_paired_predictions.csv', 'w+') as f:
    for customer_id, paired_predictions in customer_paired_predictions.items():
        f.write(customer_id)
        for rec_product in paired_predictions:
            f.write(',%s:%s' % (rec_product[0], str(rec_product[1])))
        f.write('\n')
