import joblib

# Load the pipeline
model = joblib.load('model.pkl')

# Define a test sample (same number of features as training data)
sample = [[14.2, 20.1, 90.3, 600.5, 0.095]]

# Predict using the pipeline (handles scaling + model prediction)
pred = int(model.predict(sample)[0])
prob = float(model.predict_proba(sample)[0, 1])

print("Predicted Diagnosis:", pred)
print("Probability of diagnosis = 1 (disease present):", round(prob, 4))

if pred == 1:
    print("→ The model predicts: POSITIVE (likely disease).")
else:
    print("→ The model predicts: NEGATIVE (likely healthy).")
