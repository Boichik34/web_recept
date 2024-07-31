from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, EmailField, BooleanField, StringField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[Length(min=6)])
    email = EmailField('Почта', validators=[Length(min=6), Email()])
    password = StringField('Пароль', validators=[Length(min=6)])
    submit = SubmitField('Зарегистрироваться')


class AuthorizationForm(FlaskForm):
    name = StringField('Имя', validators=[Length(min=6)])
    email = EmailField('Почта', validators=[Length(min=6)])
    password = PasswordField('Пароль', validators=[Length(min=6)])
    remember = BooleanField('Запомнить меня', default=False)
    submit = SubmitField('Авторизоваться')