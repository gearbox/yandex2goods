from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField  # , TextField
from wtforms.validators import DataRequired, Email, EqualTo, URL  # , Length


class SignUp(FlaskForm):
    email = StringField('Введите ваш Email адрес', [
        Email(message='Введите корректный email адрес'),
        DataRequired(message='Это обязательное поле')
    ])
    password = PasswordField('Введите пароль', [
        DataRequired(message='Это обязательное поле'),
    ])
    password_confirm = PasswordField('Повторите пароль', [
        EqualTo('password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Подтвердить')


class Login(FlaskForm):
    email = StringField('Email', [
        Email(message='Введите корректный email адрес'),
        DataRequired(message='Это обязательное поле')
    ])
    password = StringField('Password', [
        DataRequired(message='Это обязательное поле')
    ])
    submit = SubmitField('Log In')


class CompanyProfile(FlaskForm):
    email = StringField('Email', [
        Email(message='Введите корректный email адрес'),
        DataRequired(message='Это обязательное поле')
    ])
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
    shop_outlet = StringField('ID Склада', [
        DataRequired(message='Это обязательное поле')
    ])
    submit = SubmitField('Сохранить')
