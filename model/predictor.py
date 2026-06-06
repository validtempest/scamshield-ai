import os
import joblib

from utils.preprocessing import (
    preprocess_text
)


BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..'
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    'saved_model'
)

model_path = os.path.join(
    MODEL_DIR,
    'model.pkl'
)

vectorizer_path = os.path.join(
    MODEL_DIR,
    'vectorizer.pkl'
)

# Load model
model = joblib.load(model_path)

vectorizer = joblib.load(
    vectorizer_path
)

def predict_message(message):

    cleaned_text = preprocess_text(
        message
    )

    vectorized_text = vectorizer.transform(
        [cleaned_text]
    )

    prediction = model.predict(
        vectorized_text
    )[0]

    confidence = max(
        model.predict_proba(
            vectorized_text
        )[0]
    )

    return (
        prediction,
        confidence,
        cleaned_text
    )