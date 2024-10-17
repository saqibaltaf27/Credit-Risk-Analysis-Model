import requests
import pandas as pd
import json

url = "http://127.0.0.1:8000/predict"
headers = {"Content-Type": "application/json"}

data = pd.read_csv(r'Output\Features.csv')

data = {
    'CardCode': 'C001464',
    'Open Invoice Ratio': 5.0,
    'balance_to_credit_ratio': 2,
    'Credit Utilization Ratio': 0.75
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.status_code)
print(response.json)