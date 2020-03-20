from flask_wtf import FlaskForm
# from flask_login import current_user
from wtforms import StringField, SubmitField  # , PasswordField, TextField
# from wtforms.fields.html5 import URLField
# from wtforms.widgets.html5 import URLInput
from wtforms.validators import DataRequired, url  # , URL  # , Email, EqualTo, Length


def validate_url(_form, field):
    if not field.data.startswith('http'):
        field.data = 'http://' + field.data


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
        validate_url,
        url(message='URL адрес указан с ошибкой'),
    ])
    # shop_currency = StringField('Принимаемая валюта', [
    #     DataRequired(message='Это обязательное поле')
    # ])
    # currency_rate = StringField('Курс валюты к рублю', [
    #     DataRequired(message='Это обязательное поле')
    # ])
    # shop_outlet = StringField('ID Склада', [
    #     DataRequired(message='Это обязательное поле')
    # ])
    submit = SubmitField('Сохранить')
