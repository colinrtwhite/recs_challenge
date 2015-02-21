#!/usr/bin/python

# Builds up a file of customers, each followed by a list of products that they have purchased
# Builds customer_products.csv from product_customer.csv

customer_purchases = {}
with open('data/product_customer.csv', 'rb') as f:
    for line in f:
        product, customer = line.strip().split(',')
        try:
            customer_purchases[customer].add(product)
        except:
            customer_purchases[customer] = set([product])

with open('data/customer_products.csv', 'w+') as f:
    for customer, products in customer_purchases.items():
        f.write('%s,%s\n' % (customer, ','.join(products)))
