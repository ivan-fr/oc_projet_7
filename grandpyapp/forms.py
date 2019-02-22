from config import COUNTRIES_FILE
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, SelectField
import json


class AskForm(FlaskForm):
    ask = StringField('ask', validators=[validators.DataRequired(),
                                         validators.Length(max=200)],
                      render_kw={"placeholder": "Exemple: Salut GrandPy ! "
                                                "Est-ce que tu connais "
                                                "l'adresse d'OpenClassrooms ?",
                                 "autocomplete": "off"})

    with open(COUNTRIES_FILE, "r", encoding="utf-8") as file:
        _list = [('', '')] + list((json.load(file)).items())
        countries = SelectField('Pays', choices=_list)

    submit = SubmitField('Envoyer')
