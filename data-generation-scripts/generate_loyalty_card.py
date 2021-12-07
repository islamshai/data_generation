import json

import pandas as pd

import unnest_json

data = pd.read_json('customers.json')
data.drop(['popular_items', 'most_visited_store'], axis=1, inplace=True)
data.to_json('customers_.json', orient='records')

f = open('customers_.json', )
data = json.load(f)

data = unnest_json.json_to_dataframe(data)
data = data.drop(data[data['purchase_frequency.channel'] == 'online visit'].index)

"""
  {
    "date": "2021-01-30",
    "num_customers": 34,
    "customers_without_loyalty_card": 29,
    "stamps": 10,
    "cards_completed": 3,
    "rewards_claimed": 2
  },
"""
df = data.groupby('purchase_frequency.date', as_index=False)['purchase_frequency.amount_spent'].size()
print('sss')
df.columns = ['date', 'num_customers']
df['customers_without_loyalty_card'] = df['num_customers'] * .85
df['stamps'] = df['num_customers'] * .30
df['cards_completed'] = df['num_customers'] * .09
df['rewards_claimed'] = df['num_customers'] * .05

df['customers_without_loyalty_card'] = df['customers_without_loyalty_card'].astype('int32')
df['stamps'] = df['stamps'].astype('int32')
df['cards_completed'] = df['cards_completed'].astype('int32')
df['rewards_claimed'] = df['rewards_claimed'].astype('int32')
df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
df.style.format({"date": lambda t: t.strftime("%Y-%m-%d")})

df.to_json('loyalty_cards_new.json', orient='records')
