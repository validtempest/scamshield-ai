import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
)

from model.predictor import (
    predict_message
)

while True:

    message = input(
        "\nMasukkan pesan: "
    )

    prediction, confidence, cleaned = (
        predict_message(message)
    )

    print("\nCleaned:")
    print(cleaned)

    print("\nPrediction:")
    print(prediction)

    print(
        f"Confidence: {confidence:.2%}"
    )