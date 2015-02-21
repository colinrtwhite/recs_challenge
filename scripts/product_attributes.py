import json

# Map a product_id to its category, sub-category, brand, and price range.
product_to_attributes = {}
with open('../given/train.csv', 'rb') as f:
    for line in f:
        customer_id, product_id, timestamp, category, sub_category, brand, price_range = line.strip().split(',')

        if product_id in product_to_attributes:
            continue

        product_to_attributes[product_id] = {}
        product_to_attributes[product_id]['category'] = category
        product_to_attributes[product_id]['sub_category'] = sub_category
        product_to_attributes[product_id]['brand'] = brand
        product_to_attributes[product_id]['price_range'] = price_range

with open('../given/product_to_attributes.json', 'w+') as f:
    f.write(json.dumps(product_to_attributes))