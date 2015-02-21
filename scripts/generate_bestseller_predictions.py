#!/usr/bin/python

# Generates a set of 6 predictions for each customer based upon the most popular products overall,
# (with products already purchased by each customer excluded).

most_popular_products = []
with open('data/most_popular_products.txt', 'rb') as f:
    for line in f:
        _, product = line.strip().split(' ')
        most_popular_products.append(product)

customer_purchases = {}
with open('data/customer_products.csv', 'rb') as f:
    for line in f:
        values = line.strip().split(',')
        customer_purchases[values[0]] = values[1:]

with open('data/customer_bestseller_predictions.csv', 'w+') as f:
    for customer in customer_purchases:
        products = [product for product in most_popular_products if product not in customer_purchases[customer]][:6]
        f.write('%s,%s\n' % (customer, ','.join(products)))
