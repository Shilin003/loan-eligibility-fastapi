from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd

app = FastAPI(title="Advanced Loan Eligibility Prediction API")

# Load your pre-trained model file
try:
    model = joblib.load('loan_model.pkl')
except FileNotFoundError:
    # A defensive engineering practice: catch errors gracefully if the file is missing
    model = None

# Enforce strict validation rules using Pydantic Field
class LoanRequest(BaseModel):
    age: int = Field(..., ge=18, le=100, description="Age must be between 18 and 100")
    income: float = Field(..., gt=0, description="Income must be greater than 0")
    credit_score: int = Field(..., ge=300, le=850, description="Credit score must be between 300 and 850")

@app.post("/predict")
def predict_loan(data: LoanRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model file not found on server.")
        
    # Process valid data safely
    input_data = pd.DataFrame([{
        'age': data.age,
        'income': data.income,
        'credit_score': data.credit_score
    }])
    
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    
    return {
        "loan_approved": bool(prediction),
        "approval_probability": float(probability),
        "status": "Success"
    }