# app/model.py
import joblib

MODEL_PATH = 'crop_yield_model.pkl'

def load_model():
    return joblib.load(MODEL_PATH)  # can return (model, feature_names) if stored that way


