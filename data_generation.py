import datetime
import enum
import random

from dateutil.relativedelta import relativedelta
from faker import Faker
import string
import uuid
import pandas as pd


def get_lon_lat(a):
    lon = 52.491265
    lat = 13.400000
    return [{'longitude': lon + a * .0007, 'latitude': lat + .001}]


def get_uuid(a):
    return str(uuid.uuid4())


class Foo(enum.Enum):
    ONLINE_VISIT = 'online visit'
    ONLINE_TRX = 'online trx'
    OFFLINE_TRX = 'offline trx'


def get_discount_preference(a):
    discount_preference = random.choice(['mid', 'low', 'high'])
    return discount_preference


def get_most_popular_items(a):
    popular_items = []
    items = ['Shoes Blue', 'Grey T-Shirt', 'Sneaker Socks L', 'Brown Hoodie',
             'Black Jeans', 'Yellow Cap', 'Converse']
    for i in range(3):
        most_popular_item = random.choice(items[:])
        items.remove(most_popular_item)
        popular_items.append(most_popular_item)
    return popular_items


def get_avg_feedback(a):
    return random.choice([4.5, 4.6, 4.7, 4.8, 3.9])


def random_gmail(char_num):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(13)) + "@gmail.com"


def get_purchase_frequency(a):
    fake = Faker()

    range_number = random.randint(1, 30)
    purchase = []
    for i in range(range_number):
        channel = random.choice(['online visit', 'online trx', 'offline trx'])
        if range_number < 7:
            channel = random.choice(['online trx', 'offline trx'])

        amount = random.randint(7, 70)
        if channel == 'online visit':
            amount = 1

        date = fake.date_between(start_date=(datetime.date.today() - relativedelta(months=+12)),
                                 end_date='today').strftime('%m/%d/%Y')

        purchase.append({'channel': channel,
                         'amount_spent': amount,
                         'date': date})
    return purchase


def get_latest_date(a):
    latest_date = '02/06/2021'
    for i in a:
        if i.get('date') > latest_date:
            latest_date = i.get('date')
    return latest_date


def get_number_visit(a):
    visit = 0
    for i in a:
        if i.get('channel') != 'online visit':
            visit += 1
    return visit


def get_avg_value(a):
    avg = 0
    total_entry = 0
    for i in a:
        if i.get('channel') != 'online visit':
            print(i)
            avg += i.get('amount_spent')
            total_entry += 1
    return avg / total_entry


customer_data = pd.read_json('customers.json')
customer_data = customer_data.append([customer_data] * 3, ignore_index=True)

customer_data.loc[100:, ['opt_in', 'online_profile']] = False
customer_data.loc[1:100, ['opt_in', 'online_profile']] = True
customer_data = customer_data.sample(frac=1).reset_index(drop=True)
customer_data['most_visited_store'] = customer_data.index.map(get_lon_lat)
customer_data['purchase_frequency'] = customer_data.index.map(get_purchase_frequency)
customer_data['discount_preference'] = customer_data.index.map(get_discount_preference)
customer_data['price_sensitivity'] = customer_data.index.map(get_discount_preference)
customer_data['popular_items'] = customer_data.index.map(get_most_popular_items)
customer_data['avg_feedback'] = customer_data.index.map(get_avg_feedback)
customer_data['email'] = customer_data.index.map(random_gmail)
customer_data['leaf_id'] = customer_data.index.map(get_uuid)
customer_data['number_visits'] = customer_data['purchase_frequency'].map(get_number_visit)
customer_data['last_visited_date'] = customer_data['purchase_frequency'].map(get_latest_date)
#####
customer_data['avg_basket_size'] = customer_data['purchase_frequency'].map(get_avg_value)
customer_data['loyalty_points'].fillna(3, inplace=True)

customer_data.to_json('customers.json', orient='records')
