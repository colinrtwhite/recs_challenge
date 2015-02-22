import json
from math import log

product_consistency = {}
max_consistency = 0
with open('../given/product_consistency.json', 'rb') as f:
    consistency_json = json.load(f)
    for item in consistency_json:
        # Add 1 to prevent negative numbers
        product_consistency[item[0]] = log(item[1] + 1)
        max_consistency = max(max_consistency, product_consistency[item[0]])

for item in product_consistency:
    product_consistency[item] /= max_consistency

with open('../given/product_consistency_normalised.json', 'w+') as f:
    f.write(json.dumps(product_consistency))