from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField  # , TextField
from wtforms.validators import DataRequired, Email, EqualTo, URL  # , Length


class CompanyProfile(FlaskForm):
    email = StringField('Email')
    company_name = StringField('Название компании', [
        DataRequired(message='Это обязательное поле')
    ])
    shop_name = StringField('Название магазина', [
        DataRequired(message='Это обязательное поле')
    ])
    shop_url = StringField('URL магазина', [
        DataRequired(message='Это обязательное поле'),
        URL()
    ])
    shop_currency = StringField('Принимаемая валюта', [
        DataRequired(message='Это обязательное поле')
    ])
    currency_rate = StringField('Курс валюты', [
        DataRequired(message='Это обязательное поле')
    ])
    shop_outlet = StringField('ID Склада', [
        # DataRequired(message='Это обязательное поле')
    ])
    submit = SubmitField('Сохранить')
