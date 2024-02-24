
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from Home_work.Hw_3.models import db, User
from flask_wtf import CSRFProtect
from Home_work.Hw_3.forms import LoginForm, RegistrationForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'd9ca5b03695c407165fe4c6db98de2e6e66bfa72546bf02480c49ebc806d9e0d'
csrf = CSRFProtect(app)
db.init_app(app)

@app.route('/')
def index():
    # Перенаправляем на страницу регистрации
    return redirect(url_for('register'))


# инициализация базы данных
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/login/', methods= ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        pass
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        username = form.username.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data


        if password != confirm_password:
            return 'Пароли не совпадают!'

        # Создание нового объекта User
        new_user = User(username=username, last_name=last_name, email=email)
        new_user.set_password(password)  # Установка зашифрованного пароля


        db.session.add(new_user)

        try:

            db.session.commit()
            return redirect(url_for('register_success'))
        except Exception as e:
            # Откат транзакции в случае ошибки
            db.session.rollback()
            return f'Ошибка при регистрации: {str(e)}'

    # Если метод запроса не POST или данные формы не прошли валидацию,
    # вернуть шаблон register.html
    return render_template('register.html', form=form)


@app.route('/register_success')
def register_success():
    return render_template('register_success.html')




