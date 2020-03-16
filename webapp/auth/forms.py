from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField  # , TextField
from wtforms.validators import DataRequired, Email, EqualTo, Length  # , URL


class SignUp(FlaskForm):
    name = StringField('Имя')
    email = StringField('Введите ваш Email адрес', [
        Length(min=6, message='Введите корректный email адрес'),
        Email(message='Введите корректный email адрес'),
        DataRequired(message='Это обязательное поле')
    ])
    password = PasswordField('Введите пароль', [
        DataRequired(message='Это обязательное поле'),
        Length(min=6, message='Выберите более сложный пароль')
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
    password = PasswordField('Введите пароль', [
        DataRequired(message='Это обязательное поле')
    ])
    submit = SubmitField('Log In')
