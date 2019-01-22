from flask import Flask, render_template, request
from grandpyapp.managers.parser import parse_sentence
from grandpyapp.managers.googlemaps import parse_geolocate_response
import grandpyapp.managers.wikipedia as wikipedia
import json
import logging

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')


@app.route('/')
def index():
    url = "https://maps.googleapis.com/" \
          "maps/api/js?key={}".format(app.config["GOOGLE_API_KEY"])
    return render_template('index.html', url_google_map_api=url)


@app.route('/post_ask/', methods=['POST'])
def post_ask():
    if request.form.get('ask'):
        google_maps_parsed = {}
        wikipedia_parsed = {}
        _parse_sentence = parse_sentence(request.form['ask'])

        if _parse_sentence:
            try:
                google_maps_parsed = parse_geolocate_response(_parse_sentence)

                wiki_search_list = wikipedia.search(
                    google_maps_parsed['formatted_address'], suggestion=False)

                if not wiki_search_list:
                    wiki_search_list = wikipedia.search(
                        google_maps_parsed['asked_address'], suggestion=False)

                if not wiki_search_list:
                    wiki_search_list = wikipedia.geosearch(
                        latitude=google_maps_parsed['location']['lat'],
                        longitude=google_maps_parsed['location']['lng'],
                        radius=10000
                    )

                if wiki_search_list:
                    wikipedia_page = wikipedia.page(wiki_search_list[0])
                    wikipedia_parsed['_summary'] = wikipedia_page.summary(
                        sentences=2)
                    wikipedia_parsed['url'] = wikipedia_page.url
            except Exception as e:
                logging.exception(e)

        return json.dumps({
            'google_maps_parsed': google_maps_parsed,
            'wikipedia_parsed': wikipedia_parsed
        })
