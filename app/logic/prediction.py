import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from ..configs import configs as cf


def predict_population(subject: str, years: list[int]):
    with open(cf.POPULATION_MODELS_PATH, 'rb') as file:
        models: dict[str, LinearRegression] = pickle.load(file)
    model = models[subject]
    predicted_values = [int(max(0, *model.predict([np.array([year])]))) for year in years]
    return predicted_values
