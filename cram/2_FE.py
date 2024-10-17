import numpy as np
import pandas as pd

data = pd.read_csv('Output\ETL_Data.csv')

data['Credit Utilization Ratio'] = data['Total Balance'] / data['CreditLine']
data['Recovery Rate'] = data['Recovery'] / data['SALE']
data['Open Invoice Ratio'] = data['Open Invoice'] / data['SALE']
data['sales_to_invoice_ratio'] = data['SALE'] / data['Total Invoice']
data['balance_to_credit_ratio'] = data['Total Balance'] / data['CreditLine']

data.replace([np.inf, -np.inf], np.nan, inplace=True)
data.fillna(0, inplace=True) 


print(data.head(10))

data.to_csv('Output\Features.csv')
data.to_excel('Output\Features.xlsx')
