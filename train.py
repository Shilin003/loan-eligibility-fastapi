import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Create a dummy dataset (Age, Income, Credit Score -> Approved)
data = {
    'age': [25, 45, 30, 50, 22, 35],
    'income': [50000, 120000, 30000, 95000, 25000, 80000],
    'credit_score': [710, 800, 590, 750, 600, 680],
    'approved': [1, 1, 0, 1, 0, 1]
}
df = pd.DataFrame(data)

X = df[['age', 'income', 'credit_score']]
y = df['approved']

# 2. Train the model
model = RandomForestClassifier()
model.fit(X, y)

# 3. Serialize (Save) the model to disk
joblib.dump(model, 'loan_model.pkl')
print("Model trained and saved as loan_model.pkl!")