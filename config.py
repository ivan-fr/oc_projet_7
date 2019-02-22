import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STOP_WORDS_FILE = os.path.join(BASE_DIR, "grandpyapp", "static",
                               "stop_words.json")

GOOGLE_API_KEY = "AIzaSyCIB8gP3P5S-ttaOCZQBj0efd8sSDbPqdQ"

COUNTRIES_FILE = os.path.join(BASE_DIR, "grandpyapp", "static",
                              "countries.json")

SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
