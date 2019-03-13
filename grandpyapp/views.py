import json
import logging

from flask import Flask, render_template

import grandpyapp.managers.wikipedia as wikipedia
from grandpyapp.forms import AskForm
from grandpyapp.managers.googlemaps import parse_geolocate_response
from grandpyapp.managers.parser import parse_sentence

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')


@app.route('/')
def index():
    """Render the index page."""

    ask_form = AskForm()
    url = "https://maps.googleapis.com/" \
          "maps/api/js?key={}".format(app.config["GOOGLE_API_KEY"])
    return render_template('index.html', url_google_map_api=url,
                           ask_form=ask_form)


@app.route('/post_ask/', methods=['POST'])
def post_ask():
    """traitment of the ask request
    :return google_maps and wikipedia response"""

    ask_form = AskForm()

    if ask_form.validate_on_submit():
        google_maps_parsed = {}
        wikipedia_parsed = {}
        _parse_sentence = parse_sentence(ask_form.ask.data)

        if _parse_sentence:
            try:
                if ask_form.countries.data != '':
                    google_maps_parsed = parse_geolocate_response(
                        _parse_sentence, from_country=ask_form.countries.data)
                else:
                    google_maps_parsed = parse_geolocate_response(
                        _parse_sentence)

                wiki_search_list = wikipedia.search(
                    google_maps_parsed['asked_address'], suggestion=False)

                if not wiki_search_list:
                    wiki_search_list = wikipedia.search(
                        google_maps_parsed['formatted_address'],
                        suggestion=False)

                if not wiki_search_list:
                    wiki_search_list = wikipedia.geosearch(
                        latitude=google_maps_parsed['location']['lat'],
                        longitude=google_maps_parsed['location']['lng'],
                    )

                if wiki_search_list:
                    try:
                        wikipedia_page = wikipedia.page(wiki_search_list[0])
                    except Exception:
                        wiki_search_list = wikipedia.geosearch(
                            latitude=google_maps_parsed['location']['lat'],
                            longitude=google_maps_parsed['location']['lng'],
                        )
                        wikipedia_page = wikipedia.page(wiki_search_list[0])

                    wikipedia_parsed['_summary'] = wikipedia_page.summary(
                        sentences=2)
                    wikipedia_parsed['url'] = wikipedia_page.url

            except AssertionError as e:
                logging.exception(e)

        return json.dumps({
            'google_maps_parsed': google_maps_parsed,
            'wikipedia_parsed': wikipedia_parsed
        })
