import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier   
import joblib

features = pd.read_csv(r'Output\Features.csv')

features['Default Risk'] = (
    (features['Open Invoice Ratio'] > 0.5) |
    (features['balance_to_credit_ratio'] > 0.4) |
    (features['Credit Utilization Ratio'] > 0.75)).astype(int)

X = features.drop(['Default Risk'], axis=1)
y = features['Default Risk']

categorical_columns = ['Zone', 'Group', 'CardCode', 'CardName', 'Payment Terms'] 
for col in categorical_columns:
    X[col] = X[col].astype('category')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6,
    min_child_weight=1,
    subsample=0.8,
    colsample_bytree=0.8,
    gamma=0,
    scale_pos_weight=4, 
    use_label_encoder=False,
    eval_metric='logloss',
    enable_categorical=True  
)

model.fit(X_train, y_train)

y_prediction = model.predict(X_test)
print(classification_report(y_test, y_prediction))

features.to_csv('Output\Features.csv')
features.to_excel('Output\Features.xlsx')


joblib.dump(model, r'D:\AIProjects\CRAM\cram\Model\Credit_Risk_Model.pk1')
