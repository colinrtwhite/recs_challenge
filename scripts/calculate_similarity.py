#!/usr/bin/python
import json
from multiprocessing import Process
from math import pow, sqrt


# SIMILARITY COMPUTATION
# http://www.cs.umd.edu/~samir/498/Amazon-Recommendations.pdf
# http://en.wikipedia.org/wiki/Cosine_similarity
def calculate_similarity(data_index, allow_self_similarity):
    print "CALCULATE_SIMILARITY: " + str(data_index) + ", " + str(allow_self_similarity)
    # Simply return if data_index is not valid.
    if data_index != 1 and data_index != 3 and data_index != 4 and data_index != 5 and data_index != 6:
        return None

    attribute_to_customers = {}  # Some attribute value (decided by data_index) mapped to customers through their order histories
    with open('../given/train.csv', 'rb') as f:
        for line in f:
            # data's index values: customer_id = 0, product_id = 1, timestamp = 2, category = 3, sub_category = 4, brand = 5, price_range = 6
            data = line.strip().split(',')
            customer_id = data[0]
            attribute = data[data_index]

            if attribute not in attribute_to_customers:
                attribute_to_customers[attribute] = {}

            if customer_id not in attribute_to_customers[attribute]:
                attribute_to_customers[attribute][customer_id] = 1
            else:
                attribute_to_customers[attribute][customer_id] += 1

    similarity = {}
    for attribute1, customers1 in attribute_to_customers.items():
        if attribute1 not in similarity:
            similarity[attribute1] = {}
        for attribute2, customers2 in attribute_to_customers.items():
            # Skip if the attribute values are the same or if we've already calculated their similarity.
            if ((attribute1 is attribute2) and (not allow_self_similarity)) or (attribute2 in similarity[attribute1]):
                continue

            if attribute2 not in similarity:
                similarity[attribute2] = {}

            common_customer_dimensions = set(attribute_to_customers[attribute1].keys()) & set(attribute_to_customers[attribute2].keys())

            numerator = denomerator1 = denomerator2 = 0
            for customer_id in common_customer_dimensions:
                numerator += attribute_to_customers[attribute1][customer_id] * attribute_to_customers[attribute2][customer_id]
                denomerator1 += pow(attribute_to_customers[attribute1][customer_id], 2)
                denomerator2 += pow(attribute_to_customers[attribute2][customer_id], 2)

            denomerator = sqrt(denomerator1) * sqrt(denomerator2)
            if denomerator != 0:
                similarity[attribute1][attribute2] = similarity[attribute2][attribute1] = numerator / denomerator
    print "FINISHED: " + str(data_index) + ", " + str(allow_self_similarity)
    return similarity


def calculate_product_similarity():
    with open('../given/product_similarity.json', 'w+') as f:
        f.write(json.dumps(calculate_similarity(1, False)))


def calculate_category_similarity():
    with open('../given/category_similarity.json', 'w+') as f:
        f.write(json.dumps(calculate_similarity(3, True)))


def calculate_sub_category_similarity():
    with open('../given/sub_category_similarity.json', 'w+') as f:
        f.write(json.dumps(calculate_similarity(4, True)))


def calculate_brand__similarity():
    with open('../given/brand_similarity.json', 'w+') as f:
        f.write(json.dumps(calculate_similarity(5, True)))


def calculate_price_range_similarity():
    with open('../given/price_range_similarity.json', 'w+') as f:
        f.write(json.dumps(calculate_similarity(6, True)))


# Run the generation tasks in separate processes for speed
tasks = [calculate_product_similarity,
         calculate_category_similarity,
         calculate_sub_category_similarity,
         calculate_brand__similarity,
         calculate_price_range_similarity]
for task in tasks:
    p = Process(target=task)
    p.start()