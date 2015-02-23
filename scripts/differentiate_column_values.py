with open('../given/train.csv', 'rb') as f, with open('../given/train_modified.csv', 'w+') as g:
    for line in f:
        customer_id, product_id, timestamp, category, sub_category, brand, price_range = line.strip().split(',')
        g.write('C' + customer_id + ',P' + product_id + ',' + timestamp + ',' + category + ',' + sub_category + ',B' + brand + ',PR' + price_range + '\n')
