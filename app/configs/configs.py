import os

MAX_PREDICTION_YEARS = 10
MIN_PREDICTION_YEARS = 1

COUNTRY_SETTLEMENTS_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '../../..',
                                                         'data/country_settlements.json'))
POPULATION_MODELS_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '../../..',
                                                       'data/population_models.pickle'))
