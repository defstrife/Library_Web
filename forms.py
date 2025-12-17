from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators = [DataRequired()])
    password = PasswordField('Пароль', validators = [DataRequired()])
    submit = SubmitField('Войти')

class BookForm(FlaskForm):
    title = StringField('Название', validators = [DataRequired()])
    author = SelectField('Автор', coerce = int, validators = [DataRequired()])
    genre = StringField('Жанр', validators = [DataRequired()])
    submit = SubmitField('Добавить книгу')
class OrderForm(FlaskForm):
    user_id = SelectField('Пользователь', coerce = int, validators = [DataRequired()])
    book_id = SelectField('Книга', coerce = int, validators = [DataRequired()])
    submit = SubmitField('Заказать')

class IssueForm(FlaskForm):
    user_id = SelectField('Пользователь', coerce = int, validators = [DataRequired()])
    book_id = SelectField('Книга', coerce = int, validators = [DataRequired()])
    submit = SubmitField('Выдать книгу')