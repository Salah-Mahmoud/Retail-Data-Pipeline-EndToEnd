import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)
np.random.seed(42)

num_records = 5000
num_stores = 20
num_promotions = 20
num_products = 50
num_customers = 200


categories = ['Electronics', 'Clothing', 'Home Goods', 'Beauty', 'Toys']
store_types = ['Boutique', 'Supermarket', 'Department Store', 'Online']
payment_types = ['debit card', 'credit card', 'Cash', 'Mobile Payment']
providers = ['Visa', 'MasterCard', 'Maestro', 'PayPal', 'Amex']
promotion_types = ['Seasonal', 'Clearance', 'Loyalty', 'Holiday']

customer_ids = [f"CUST_{i:06d}" for i in range(1, num_customers + 1)]
product_ids = [f"PROD_{i:06d}" for i in range(1, num_products + 1)]
store_ids = [f"STORE_{i:06d}" for i in range(1, num_stores + 1)]
promotion_ids = [f"PROMO_{i:06d}" for i in range(1, num_promotions + 1)]

stores = [{
    'StoreID': store_ids[i],
    'StoreName': fake.company(),
    'StoreLocation': fake.street_address() + ", " + fake.city() + ", " + fake.state() + " " + fake.zipcode(),
    'StoreType': random.choice(store_types),
    'OpeningDate': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
    'ManagerName': fake.name()
} for i in range(num_stores)]
store_df = pd.DataFrame(stores)

promotion_versions = []
for promotion_id in promotion_ids:
    num_versions = random.randint(2, 5)
    base_date = fake.date_between(start_date='-1y', end_date='-6M')
    promotion_type = random.choice(promotion_types)
    promotion_name = fake.catch_phrase() + "!"
    for i in range(num_versions):
        updated_at = base_date + timedelta(days=30 * i)
        promotion_versions.append({
            'PromotionID': promotion_id,
            'PromotionName': promotion_name,
            'PromotionType': promotion_type,
            'DiscountPercentage': round(random.uniform(5.0, 50.0), 2),
            'PromotionStartDate': (base_date + timedelta(days=30 * i)).strftime('%Y-%m-%d'),
            'UpdatedAt': updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })
promotion_df = pd.DataFrame(promotion_versions)

product_versions = []
for product_id in product_ids:
    num_versions = random.randint(2, 4)
    base_date = fake.date_between(start_date='-1y', end_date='-6M')
    product_name = fake.word().capitalize() + " (" + random.choice(['New', 'Refurbished']) + ")"
    category = random.choice(categories)
    for i in range(num_versions):
        updated_at = base_date + timedelta(days=30 * i)
        product_versions.append({
            'ProductID': product_id,
            'ProductName': product_name,
            'Category': category,
            'Price': round(random.uniform(10.0, 1000.0), 2),
            'UpdatedAt': updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })
product_df = pd.DataFrame(product_versions)

customers = [{
    'CustomerID': cid,
    'FirstName': fake.first_name(),
    'LastName': fake.last_name(),
    'Email': fake.email(),
    'PhoneNumber': fake.phone_number(),
    'Address': fake.street_address() + ", " + fake.city() + ", " + fake.state() + " " + fake.zipcode(),
    'City': fake.city(),
    'State': fake.state(),
    'Country': fake.country(),
    'ZipCode': fake.zipcode()
} for cid in customer_ids]
customer_df = pd.DataFrame(customers)

start_date = datetime.strptime('2020-01-01', '%Y-%m-%d').date()
end_date = datetime.strptime('2024-12-31', '%Y-%m-%d').date()
orders = []
payments = []

for i in range(num_records):
    customer_id = random.choice(customer_ids)
    product = product_df.sample(1).iloc[0]
    price = product['Price']
    quantity_sold = random.randint(1, 10)
    total_sales = round(price * quantity_sold, 2)
    store = store_df.sample(1).iloc[0]
    promotion = promotion_df.sample(1).iloc[0]
    discount_percentage = promotion['DiscountPercentage']
    discount_amount = round(total_sales * (discount_percentage / 100), 2)
    net_sales = round(total_sales - discount_amount, 2)
    purchase_date = fake.date_between(start_date=start_date, end_date=end_date)
    date_id = f"DATE_{purchase_date.strftime('%Y%m%d')}"
    payment_id = f"PAY_{i:06d}"

    payments.append({
        'PaymentMethodID': payment_id,
        'PaymentType': random.choice(payment_types),
        'Provider': random.choice(providers)
    })

    orders.append({
        'OrderID': f"ORDER_{i:06d}",
        'CustomerID': customer_id,
        'ProductID': product['ProductID'],
        'StoreID': store['StoreID'],
        'PromotionID': promotion['PromotionID'],
        'PaymentMethodID': payment_id,
        'DateID': date_id,
        'PurchaseDate': purchase_date.strftime('%Y-%m-%d'),
        'QuantitySold': quantity_sold,
        'TotalSales': total_sales,
        'DiscountAmount': discount_amount,
        'NetSales': net_sales
    })

orders_df = pd.DataFrame(orders)
payment_df = pd.DataFrame(payments)

store_df.to_csv('store.csv', index=False)
customer_df.to_csv('customer.csv', index=False)
orders_df.to_csv('orders.csv', index=False)
payment_df.to_csv('payment.csv', index=False)
promotion_df.to_csv('promotion.csv', index=False)
product_df.to_csv('product.csv', index=False)
