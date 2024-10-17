from fastapi import FastAPI
import joblib
import pandas as pd

model = joblib.load(r'D:\AIProjects\CRAM\cram\Model\Credit_Risk_Model.pk1')

app = FastAPI()

@app.post("/predict")
def predict_risk(customer_id: int, open_invoice_ratio: float, credit_utilization_ratio: float, recovery_rate: float):
    input_data =pd.DataFrame([{
        'Open Invoice Ratio' : open_invoice_ratio,
        'Credit Utilization Ratio' : credit_utilization_ratio,
        'Recovery Rate': recovery_rate
    }])
    
    prediction = model.predict(input_data)[0]
    
    return {"customer_id": customer_id, "default_risk": int(prediction)}


