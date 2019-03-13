import json
import logging

from flask import Flask, render_template
from flask.views import MethodView

from grandpyapp.managers.wikipedia import WikipediaFunction
from grandpyapp.forms import AskForm
from grandpyapp.managers.googlemaps import GoogleFunction
from grandpyapp.managers.parser import parse_sentence

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')


class IndexView(MethodView):
    def get(self):
        """Render the index page."""

        ask_form = AskForm()
        url = "https://maps.googleapis.com/" \
              "maps/api/js?key={}".format(app.config["GOOGLE_API_KEY"])
        return render_template('index.html', url_google_map_api=url,
                               ask_form=ask_form)

    def post(self):
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
                        google_maps_parsed = GoogleFunction.parse_geolocate(
                            _parse_sentence,
                            from_country=ask_form.countries.data)
                    else:
                        google_maps_parsed = GoogleFunction.parse_geolocate(
                            _parse_sentence)

                    wiki_search_list = WikipediaFunction.search(
                        google_maps_parsed['asked_address'], suggestion=False)

                    if not wiki_search_list:
                        wiki_search_list = WikipediaFunction.search(
                            google_maps_parsed['formatted_address'],
                            suggestion=False)

                    if not wiki_search_list:
                        wiki_search_list = WikipediaFunction.geosearch(
                            latitude=google_maps_parsed['location']['lat'],
                            longitude=google_maps_parsed['location']['lng'],
                        )

                    if wiki_search_list:
                        try:
                            wikipedia_page = WikipediaFunction.page(
                                wiki_search_list[0])
                        except Exception:
                            wiki_search_list = WikipediaFunction.geosearch(
                                latitude=google_maps_parsed['location']['lat'],
                                longitude=google_maps_parsed['location']['lng'],
                            )
                            wikipedia_page = WikipediaFunction.page(
                                wiki_search_list[0])

                        wikipedia_parsed['_summary'] = wikipedia_page.summary(
                            sentences=2)
                        wikipedia_parsed['url'] = wikipedia_page.url

                except AssertionError as e:
                    logging.exception(e)

            return json.dumps({
                'google_maps_parsed': google_maps_parsed,
                'wikipedia_parsed': wikipedia_parsed
            })


app.add_url_rule('/', view_func=IndexView.as_view('index'))
