data/most_popular_products.txt: given/train.csv
	cut -d , -f2 given/train.csv | sort | uniq -c | sort -k1 -n -r | head -n 50 > data/most_popular_products.txt

data/product_customer.csv: given/train.csv
	awk -F "," '{ print $$2","$$1 }' given/train.csv > data/product_customer.csv

data/customer_bestseller_predictions.csv: data/most_popular_products.txt data/customer_products.csv
	python scripts/generate_bestseller_predictions.py

data/customer_paired_predictions.csv: given/product_consistency.json given/item_to_item_collaborative_similarity.json data/customer_products.csv
	python scripts/generate_paired_predictions.py

data/customer_products.csv: data/product_customer.csv
	python scripts/customer_purchases.py

data/paired_products.csv: data/product_customer.csv
	python scripts/product_pairs.py

overall_output.csv: given/customers_to_predict.csv data/customer_products.csv data/customer_bestseller_predictions.csv data/customer_paired_predictions.csv
	python scripts/combine_result_sets.py

clean:
	rm -f overall_output.csv
	rm -rf data
	mkdir data

all: overall_output.csv