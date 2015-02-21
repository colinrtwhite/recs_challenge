#!/usr/bin/python

from collections import defaultdict
import operator

# Calculates which products are strongly paired, based on how often they were bought together in all customers' order
# histories.

# Very similar to scripts/customer_to_products.py except we do not want to disregard order.
customer_purchases = {}
with open('data/product_customer.csv', 'rb') as f:
    for line in f:
        product, customer = line.strip().split(',')
        if customer in customer_purchases:
            customer_purchases[customer].append(product)
        else:
            customer_purchases[customer] = [product]
       

product_pairs = defaultdict(lambda: defaultdict(int))
for customer, products in customer_purchases.items():
    next_index = 1
    size = len(products)
    for product in products:
        if next_index != size:
            pair = (product, products[next_index])
            product_pairs[pair[0]][pair[1]] += 1.0
            product_pairs[pair[1]][pair[0]] += 1.0

        next_index = next_index + 1

# The format in paired_products.csv is:
# product_id, (other_product_id : num_times_they_appear_in_same_order_history)*
# The other_product_id:frequency pairs are sorted in decreasing order by frequency
# NOTE: Not sure how, but paired_products.csv does not contain any self pairs.
with open('data/paired_products.csv', 'w+') as f:
    for product, paired_products in product_pairs.items():
        sorted_paired = sorted(paired_products.items(), key = operator.itemgetter(1), reverse = True)

        f.write(str(product))
        for t in sorted_paired:
            f.write(',%s:%s' % (t[0], str(t[1])))
        f.write('\n')
