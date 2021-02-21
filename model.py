
import os
import joblib


class Classifier():
    def __init__(self, model_path):
        self.model = None
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)

    def predict(self, text):
        if self.model is None:
            return "unclassified"
        print(self.model.predict_proba([text]))
        return self.model.predict([text])
