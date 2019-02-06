import json
import urllib.request
from io import BytesIO
from decimal import Decimal
from grandpyapp.managers import wikipedia
import pytest


class TestSearchLoc:
    """Test the functionality of wikipedia.geosearch."""

    @classmethod
    def setup_class(cls):
        cls.mock_data = {
            "data": {
                "geo_search": ['Great Wall of China'],
                "geo_search_with_radius":
                    ['Great Wall of China', 'Jinshanling', 'Gubeikou'],
                "geo_search_with_existing_article_name":
                    ['Great Wall of China'],
                "geo_search_with_non_existing_article_name":
                    [],
            },
            "requests": {
                "geo_search": {'batchcomplete': '', 'query': {'geosearch': [
                    {'pageid': 5094570, 'ns': 0,
                     'title': 'Great Wall of China', 'lat': 40.68,
                     'lon': 117.23, 'dist': 378.2, 'primary': ''}]}},
                "geo_search_with_radius": {'batchcomplete': '', 'query': {
                    'geosearch': [{'pageid': 5094570, 'ns': 0,
                                   'title': 'Great Wall of China',
                                   'lat': 40.68, 'lon': 117.23,
                                   'dist': 378.2, 'primary': ''},
                                  {'pageid': 10135375, 'ns': 0,
                                   'title': 'Jinshanling',
                                   'lat': 40.676388888889,
                                   'lon': 117.24444444444, 'dist': 1057.1,
                                   'primary': ''},
                                  {'pageid': 34692121, 'ns': 0,
                                   'title': 'Gubeikou', 'lat': 40.692169,
                                   'lon': 117.16382, 'dist': 5987.8,
                                   'primary': ''}]}},
                "geo_search_with_non_existing_article_name": {
                    "batchcomplete": "", "query": {
                        "normalized": [
                            {"from": "fdosfjdspdj", "to": "Fdosfjdspdj"}],
                        "pages": {"-1": {"ns": 0, "title": "Fdosfjdspdj",
                                         "missing": ""}}, "geosearch": [
                            {"pageid": 5094570, "ns": 0,
                             "title": "Great Wall of China", "lat": 40.68,
                             "lon": 117.23, "dist": 378.2, "primary": ""}]}}
            }
        }

    def test_geosearch(self, monkeypatch):
        """Test parsing a Wikipedia location request result."""

        def mockreturn(request):
            return BytesIO(json.dumps(
                self.mock_data['requests']["geo_search"]).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        assert wikipedia.geosearch(Decimal('40.67693'), Decimal('117.23193')) \
               == self.mock_data['data']["geo_search"]

    def test_geosearch_with_radius(self, monkeypatch):
        """Test parsing a Wikipedia location request result."""

        def mockreturn(request):
            return BytesIO(json.dumps(
                self.mock_data['requests']["geo_search_with_radius"]).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        assert wikipedia.geosearch(
            Decimal('40.67693'), Decimal('117.23193'), radius=10000) == \
               self.mock_data['data']["geo_search_with_radius"]

    def test_geosearch_with_existing_title(self, monkeypatch):
        """Test parsing a Wikipedia location request result."""

        def mockreturn(request):
            return BytesIO(json.dumps(
                self.mock_data['requests']["geo_search"]).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        assert wikipedia.geosearch(
            Decimal('40.67693'), Decimal('117.23193'),
            title='Great Wall of China') == \
               self.mock_data['data']["geo_search_with_existing_article_name"]

    def test_geosearch_with_non_existing_title(self, monkeypatch):
        """Test parsing a Wikipedia location request result."""

        def mockreturn(request):
            return BytesIO(json.dumps(
                self.mock_data['requests']["geo_search_with_non_"
                                           "existing_article_name"]).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        assert wikipedia.geosearch(
            Decimal('40.67693'), Decimal('117.23193'), title='fdosfjdspdj') == \
               self.mock_data['data']["geo_search_with_non_"
                                      "existing_article_name"]


class TestSearch:
    """Test the functionality of wikipedia.search."""

    @classmethod
    def setup_class(cls):
        cls.mock_data = {
            "data": {
                "barack.search": ['Barack Obama',
                                  'Family of Barack Obama',
                                  'Barack Obama Sr.',
                                  'Presidency of Barack Obama',
                                  "Barack Obama citizenship"
                                  " conspiracy theories",
                                  'Speeches of Barack Obama',
                                  "First inauguration "
                                  "of Barack Obama",
                                  "Barack Obama religion"
                                  " conspiracy theories",
                                  "Barack Obama"
                                  " Presidential Center",
                                  "Early life and career"
                                  " of Barack Obama"]
            },
            "requests": {
                "barack": {
                    "batchcomplete": "",
                    "continue": {"sroffset": 10, "continue": "-||"},
                    "query": {"searchinfo": {"totalhits": 19127},
                              "search": [
                                  {"ns": 0, "title": "Barack Obama",
                                   "pageid": 534366},
                                  {"ns": 0,
                                   "title": "Family of Barack Obama",
                                   "pageid": 17775180},
                                  {"ns": 0, "title": "Barack Obama Sr.",
                                   "pageid": 16136849},
                                  {"ns": 0,
                                   "title": "Presidency of Barack Obama",
                                   "pageid": 20082093},
                                  {"ns": 0,
                                   "title": "Barack Obama citizenship"
                                            " conspiracy theories",
                                   "pageid": 20617631},
                                  {"ns": 0,
                                   "title": "Speeches of Barack Obama",
                                   "pageid": 37825066},
                                  {"ns": 0,
                                   "title": "First inauguration "
                                            "of Barack Obama",
                                   "pageid": 20767983},
                                  {"ns": 0,
                                   "title": "Barack Obama religion"
                                            " conspiracy theories",
                                   "pageid": 26472604},
                                  {"ns": 0,
                                   "title": "Barack Obama"
                                            " Presidential Center",
                                   "pageid": 41828619},
                                  {"ns": 0,
                                   "title": "Early life and career"
                                            " of Barack Obama",
                                   "pageid": 16394033}]}
                },
                'porsche': {
                    'batchcomplete': '',
                    'continue': {'sroffset': 3, 'continue': '-||'},
                    'query': {'searchinfo': {'totalhits': 7686},
                              'search': [
                                  {'ns': 0, 'title': 'Porsche',
                                   'pageid': 24365},
                                  {'ns': 0, 'title': 'Porsche 911',
                                   'pageid': 48345830},
                                  {'ns': 0,
                                   'title': 'Ferdinand Porsche',
                                   'pageid': 67720}]}
                },
                'hallelulejah': {
                    'batchcomplete': '', 'query': {
                        'searchinfo': {
                            'suggestion': 'hallelujah',
                            'suggestionsnippet': '<em>hallelujah</em>'
                        },
                        'search': []}
                },
                'qmxjsudek': {'batchcomplete': '', 'query': {'search': []}}
            }
        }

    def test_search(self, monkeypatch):
        """Test parsing a Wikipedia request result."""

        def mockreturn(request):
            return BytesIO(json.dumps(
                self.mock_data['requests']["barack"]).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        assert wikipedia.search("Barack Obama") == \
               self.mock_data['data']["barack.search"]

    def test_limit(self, monkeypatch):
        """Test limiting a request results."""

        def mockreturn(request):
            return BytesIO(json.dumps(
                self.mock_data['requests']["porsche"]).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        assert len(wikipedia.search("Porsche", results=3)) <= 3

    def test_suggestion(self, monkeypatch):
        """Test getting a suggestion as well as search results."""

        def mockreturn(request):
            return BytesIO(json.dumps(
                self.mock_data['requests']["hallelulejah"]).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        search, suggestion = wikipedia.search("hallelulejah", suggestion=True)
        assert search == []
        assert suggestion == "hallelujah"

    def test_suggestion_none(self, monkeypatch):
        """Test getting a suggestion when there is no suggestion."""

        def mockreturn(request):
            return BytesIO(json.dumps(
                self.mock_data['requests']["qmxjsudek"]).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        search, suggestion = wikipedia.search("qmxjsudek", suggestion=True)
        assert search == []
        assert suggestion is None


class TestPageSetUp:
    """Test the functionality of
    wikipedia.page's __init__ and load functions."""

    @classmethod
    def setup_class(cls):
        cls.mock_data = {
            "requests": {
                "missing": {
                    'query': {'normalized': [
                        {'from': 'sdfjpodsjdf', 'to': 'Sdfjpodsjdf'}],
                        'pages':
                            {'-1': {'ns': 0, 'title': 'Sdfjpodsjdf',
                                    'missing': ''}}}
                },
                "redirect_true_1": {'query': {'redirects': [
                    {'to': 'Edison, New Jersey',
                     'from': 'Menlo Park, New Jersey'}], 'pages': {
                    '125414': {'lastrevid': 607768264, 'pageid': 125414,
                               'title': 'Edison, New Jersey', }}}
                },
                "redirect_true_2": {
                    'query': {'pages': {
                        '125414':
                            {'pageid': 125414, 'ns': 0,
                             'title': 'Edison, New Jersey',
                             'contentmodel': 'wikitext',
                             'pagelanguage': 'en',
                             'fullurl': 'https://en.wikipedia.org'
                                        '/wiki/Edison,_New_Jersey',
                             }}}
                },
                'norm_1': {'query': {'normalized': [
                    {'from': 'communist Party', 'to': 'Communist Party'}],
                    'redirects': [{
                        'from': 'Communist Party',
                        'to': 'Communist party'}],
                    'pages': {'37008': {
                        'pageid': 37008,
                        'ns': 0,
                        'title': 'Communist party',
                        'contentmodel': 'wikitext',
                        'pagelanguage': 'en',
                        'pagelanguagehtmlcode': 'en',
                        'pagelanguagedir': 'ltr',
                        'touched': '2019-01-21T18:36:45Z',
                        'lastrevid': 874783101,
                        'length': 10447}}}},
                'norm_2': {'query': {'pages': {
                    '37008': {'pageid': 37008, 'ns': 0,
                              'title': 'Communist party',
                              'contentmodel': 'wikitext', 'pagelanguage': 'en',
                              'pagelanguagehtmlcode': 'en',
                              'pagelanguagedir': 'ltr',
                              'touched': '2019-01-21T18:36:45Z',
                              'lastrevid': 874783101, 'length': 10447,
                              'fullurl': 'https://en.wikipedia.org/wiki/'
                                         'Great_Wall_of_China'}}}}
            }
        }

    def test_missing(self, monkeypatch):
        """Test that page raises a PageError for a nonexistant page."""

        def mockreturn(request):
            return BytesIO(json.dumps(self.mock_data["requests"]["missing"])
                           .encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        with pytest.raises(Exception):
            wikipedia.page("sdfjpodsjdf", auto_suggest=False)

    def test_redirect_true(self, monkeypatch):
        """Test that a page successfully redirects a query."""

        def mockreturn(request):
            if "Menlo" in request:
                mock_data = self.mock_data["requests"]["redirect_true_1"]
            else:
                mock_data = self.mock_data["requests"]["redirect_true_2"]
            return BytesIO(json.dumps(mock_data).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        # no error should be raised if redirect is true
        mp = wikipedia.page("Menlo Park, New Jersey", auto_suggest=False)

        assert mp.title == "Edison, New Jersey"
        assert mp.url == "https://en.wikipedia.org/wiki/Edison,_New_Jersey"

    def test_redirect_false(self, monkeypatch):
        """Test that page raises an error
         on a redirect when redirect == False."""

        def mockreturn(request):
            mock_data = self.mock_data["requests"]["redirect_true_1"]
            return BytesIO(json.dumps(mock_data).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        with pytest.raises(Exception):
            wikipedia.page("Menlo Park, New Jersey",
                           auto_suggest=False, redirect=False)

    def test_redirect_with_normalization(self, monkeypatch):
        """Test that a page redirect with a normalized query loads correctly"""

        def mockreturn(request):
            if "Party" in request:
                mock_data = self.mock_data["requests"]["norm_1"]
            else:
                mock_data = self.mock_data["requests"]["norm_2"]
            return BytesIO(json.dumps(mock_data).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        the_party = wikipedia.page("communist Party", auto_suggest=False)
        assert isinstance(the_party, wikipedia.WikipediaPage)
        assert the_party.title == "Communist party"


class TestPage:
    """Test the functionality of the rest of wikipedia.page."""

    @classmethod
    def setup_class(cls):
        cls.mock_data = {
            "data": {
                "celtuce.summary": 'Celtuce (Lactuca sativa var. asparagina,'
                                   ' augustana, or angustata), also called stem'
                                   ' lettuce, celery lettuce,'
                                   ' asparagus lettuce,'
                                   ' or Chinese lettuce, IPA (UK,US)'
                                   ' /\u02c8s\u025blt.\u0259s/, is a '
                                   'cultivar of lettuce grown primarily '
                                   'for its thick stem, used '
                                   'as a vegetable. It '
                                   'is especially popular '
                                   'in China, and is called'
                                   ' wosun (Chinese: \u83b4\u7b0b; pinyin:'
                                   ' w\u014ds\u016dn) or woju (Chinese:'
                                   ' \u83b4\u82e3; pinyin:'
                                   ' w\u014dj\xf9) (although '
                                   'the latter name may also'
                                   ' be used to mean lettuce'
                                   ' in general).\n\nThe stem'
                                   ' is usually harvested '
                                   'at a length of around 15\u201320 cm and a '
                                   'diameter of around'
                                   ' 3\u20134 cm. It is crisp, '
                                   'moist, and mildly flavored, and typically '
                                   'prepared by slicing and then stir frying '
                                   'with more strongly flavored ingredients.',
                "cyclone.summary": 'Tropical Depression '
                                   'Ten was the tenth tropical'
                                   ' cyclone of the record-breaking'
                                   ' 2005 Atlantic '
                                   'hurricane season. It '
                                   'formed on August 13 from '
                                   'a tropical wave that emerged from the west '
                                   'coast of Africa on '
                                   'August 8. As a result of '
                                   'strong wind shear, the'
                                   ' depression remained weak'
                                   ' and did not strengthen beyond tropical '
                                   'depression status. The cyclone degenerated '
                                   'on August 14, although'
                                   ' its remnants partially '
                                   'contributed to the formation of Tropical '
                                   'Depression Twelve, which'
                                   ' eventually intensified'
                                   ' into Hurricane Katrina. The cyclone had no'
                                   ' effect on land, and did not directly '
                                   'result in any fatalities or damage.',
            },
            "requests": {
                "celtuce": {'query': {'pages': {
                    '1868108': {'pageid': 1868108, 'ns': 0, 'title': 'Celtuce',
                                'contentmodel': 'wikitext',
                                'pagelanguage': 'en',
                                'pagelanguagehtmlcode': 'en',
                                'pagelanguagedir': 'ltr',
                                'touched': '2019-01-19T11:10:22Z',
                                'lastrevid': 870110722, 'length': 4509,
                                'fullurl': 'https://en.wikipedia.org'
                                           '/wiki/Celtuce'}}}},
                "cyclone": {'query': {'pages': {
                    '21196082': {'pageid': 21196082, 'ns': 0,
                                 'title': 'Tropical Depression Ten (2005)',
                                 'contentmodel': 'wikitext',
                                 'pagelanguage': 'en',
                                 'pagelanguagehtmlcode': 'en',
                                 'pagelanguagedir': 'ltr',
                                 'touched': '2019-01-19T11:44:46Z',
                                 'lastrevid': 876343006, 'length': 8624,
                                 'fullurl': 'https://en.wikipedia.org/wiki/Tro'
                                            'pical_Depression_Ten_(2005)'}}}},
                "great_wall_of_china": {'query': {
                    'pages':
                        {'5094570': {'pageid': 5094570, 'ns': 0,
                                     'title': 'Great Wall of China',
                                     'contentmodel': 'wikitext',
                                     'pagelanguage': 'en',
                                     'pagelanguagehtmlcode': 'en',
                                     'pagelanguagedir': 'ltr',
                                     'touched': '2019-01-21T10:49:28Z',
                                     'lastrevid': 879400675,
                                     'length': 53591,
                                     'fullurl': 'https://en.wikipedia.org/wiki/'
                                                'Great_Wall_of_China'}}}},
                "summary_celtuce": {'query': {'pages': {'1868108': {
                    'extract': 'Celtuce (Lactuca sativa var. asparagina,'
                               ' augustana, or angustata), also called stem'
                               ' lettuce, celery lettuce, asparagus lettuce,'
                               ' or Chinese lettuce, IPA (UK,US)'
                               ' /\u02c8s\u025blt.\u0259s/, is a '
                               'cultivar of lettuce grown primarily '
                               'for its thick stem, used as a vegetable. It '
                               'is especially popular in China, and is called'
                               ' wosun (Chinese: \u83b4\u7b0b; pinyin:'
                               ' w\u014ds\u016dn) or woju (Chinese:'
                               ' \u83b4\u82e3; pinyin: w\u014dj\xf9) (although '
                               'the latter name may also'
                               ' be used to mean lettuce'
                               ' in general).\n\nThe stem is usually harvested '
                               'at a length of around 15\u201320 cm and a '
                               'diameter of around 3\u20134 cm. It is crisp, '
                               'moist, and mildly flavored, and typically '
                               'prepared by slicing and then stir frying '
                               'with more strongly flavored ingredients.',
                    'ns': 0, 'pageid': 1868108, 'title': 'Celtuce'}}}},
                "summary_depression": {'query': {'pages': {'21196082': {
                    'extract': 'Tropical Depression Ten was the tenth tropical'
                               ' cyclone of the record-breaking 2005 Atlantic '
                               'hurricane season. It formed on August 13 from '
                               'a tropical wave that emerged from the west '
                               'coast of Africa on August 8. As a result of '
                               'strong wind shear, the depression remained weak'
                               ' and did not strengthen beyond tropical '
                               'depression status. The cyclone degenerated '
                               'on August 14, although its remnants partially '
                               'contributed to the formation of Tropical '
                               'Depression Twelve, which eventually intensified'
                               ' into Hurricane Katrina. The cyclone had no'
                               ' effect on land, and did not directly '
                               'result in any fatalities or damage.',
                    'ns': 0, 'pageid': 21196082,
                    'title': 'Tropical Depression Ten (2005)'}}}},

            }
        }

    @pytest.fixture(autouse=True)
    def setup_method(self, monkeypatch):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """

        # shortest wikipedia articles with images and sections
        def mockreturn(request):
            mock_data = self.mock_data["requests"]["celtuce"]
            return BytesIO(json.dumps(mock_data).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        self.celtuce = wikipedia.page("Celtuce", auto_suggest=False)

        def mockreturn(request):
            mock_data = self.mock_data["requests"]["cyclone"]
            return BytesIO(json.dumps(mock_data).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        self.cyclone = wikipedia.page("Tropical Depression Ten (2005)",
                                      auto_suggest=False)

        def mockreturn(request):
            mock_data = self.mock_data["requests"]["great_wall_of_china"]
            return BytesIO(json.dumps(mock_data).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        self.great_wall_of_china = wikipedia.page("Great Wall of China",
                                                  auto_suggest=False)

    def test_from_page_id(self, monkeypatch):
        """Test loading from a page id"""

        def mockreturn(request):
            mock_data = self.mock_data["requests"]["celtuce"]
            return BytesIO(json.dumps(mock_data).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        assert self.celtuce == wikipedia.page(pageid=1868108)

    def test_title(self):
        """Test the title."""
        assert self.celtuce.title == "Celtuce"
        assert self.cyclone.title == "Tropical Depression Ten (2005)"

    def test_url(self):
        """Test the url."""
        assert self.celtuce.url == "https://en.wikipedia.org/wiki/Celtuce"
        assert self.cyclone.url == "https://en.wikipedia.org/wiki/" \
                                   "Tropical_Depression_Ten_(2005)"

    def test_summary(self, monkeypatch):
        """Test the summary."""

        def mockreturn(request):
            mock_data = self.mock_data["requests"]["summary_celtuce"]
            return BytesIO(json.dumps(mock_data).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        assert self.celtuce.summary() == self.mock_data['data'][
            "celtuce.summary"]

        def mockreturn(request):
            mock_data = self.mock_data["requests"]["summary_depression"]
            return BytesIO(json.dumps(mock_data).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        assert self.cyclone.summary() == self.mock_data['data'][
            "cyclone.summary"]
