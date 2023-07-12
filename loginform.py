from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SubmitField
from wtforms.validators import DataRequired


# from wtforms import FileField
# Если из формы добавлен файл, то обращаться к нему при обработке формы следует так:
# f.form <название поля с файлом>.data

class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    #   file = FileField('Файл')
    submit = SubmitField('Войти')

