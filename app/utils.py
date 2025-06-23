import pandas as pd

def prepare_input(rainfall, temperature, pesticide, feature_names):
    input_dict = {
        'Rainfall': rainfall,
        'Temperature': temperature,
        'Pesticide_Use': pesticide
    }
    df = pd.DataFrame([input_dict])
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0
    return df[feature_names]


