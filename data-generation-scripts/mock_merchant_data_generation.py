import json

import pandas as pd

import unnest_json
# Opening JSON file


data = pd.read_json('customers.json')
data.drop(['popular_items', 'most_visited_store'], axis=1, inplace=True)
data.to_json('customers_.json',  orient='records')

f = open('customers_.json', )

# returns JSON object as
# a dictionary
data = json.load(f)

data = unnest_json.json_to_dataframe(data)
data = data.drop(data[data['purchase_frequency.channel'] == 'online visit'].index)
df1 = data.groupby('purchase_frequency.date', as_index=False)['purchase_frequency.amount_spent'].sum()
df1['uplift_value'] = df1['purchase_frequency.amount_spent']*.053

df1.columns = ['date', 'transaction_amount', 'uplift_value']
df1.to_json('customer_lifetime_value.json', orient='records')

df = pd.DataFrame()
df['date'] = df1['date']
df['transaction_amount'] = df1['transaction_amount']*.2
df['uplift_value'] = df['transaction_amount']*.053
df.to_json('loyalty_card_clv.json', orient='records')


