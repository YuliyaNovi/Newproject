from flask import Flask, request, redirect, abort
from flask import render_template, make_response, session
import json
import requests

from forms.add_news import NewsForm
from loginform import LoginForm
from data import db_session
from data.users import User
from data.news import News
from forms.user import RegisterForm
import datetime
from mail_sender import send_mail
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'too short key'
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///db/news.sqlite'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)  # создать сессию на год


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/')
@app.route('/index')
# @login_required  # запретить страницу для не авторизированного пользователя
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter((News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    # db_sess = db_session.create_session()
    # news = db_sess.query(News).filter(News.is_private != True)
    return render_template('index.html', title='Новости', news=news)  # * список **словарь


#  return render_template('index.html', title='Работа с шаблонами', username=user)

#  return redirect('/load_photo')  # безусловный редирект, сразу кидает пользователя на страницу с главной
@app.errorhandler(404)
def http_404_error(error):
    return redirect('/error404')


@app.route('/error404')
def well():  # колодец
    return render_template('well.html')


@app.errorhandler(401)
def http_401_handler(error):
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():  # все ли введено в форме
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Проблема с регистрацией', message='Пароли не совпадают',
                                   form=form)

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Проблема с регистрацией',
                                   message='Такой пользователь уже есть', form=form)
        user = User(name=form.name.data, email=form.email.data, about=form.about.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Неверный логин или пароль', title='Повторная авторизация',
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/cookie_test')
def cookie_test():
    visit_count = int(request.cookies.get('visit_count', 0))
    if visit_count != 0 and visit_count <= 15:
        res = make_response(f'Были тут {visit_count + 1} раз')
        res.set_cookie('visit_count', str(visit_count + 1), max_age=60 * 60 * 24 * 365 * 2)
    #  скинуть счетчик куки
    elif visit_count > 15:
        res = make_response(f'Были тут {visit_count + 1} раз')
        res.set_cookie('visit_count', '1', max_age=0)
    else:
        res = make_response('Вы впервые тут за 2 года')
        res.set_cookie('visit_count', '1', max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route('/session_test')
def session_test():
    visit_count = session.get('visit_count', 0)
    session['visit_count'] = visit_count + 1
    if session['visit_count'] > 3:
        session.pop('visit_count', None)  # принудительно убить сессию
    session.permanent = True  # не убивать сессию после закрытия браузера 31 день
    return make_response(f'Мы тут были уже {visit_count + 1} раз')


@app.route('/success')
def success():
    return 'Success'


@app.route('/weather_form', methods=['GET', 'POST'])
def weather_form():
    if request.method == 'GET':
        return render_template('weather_form.html', title="Погода")
    elif request.method == 'POST':
        town = request.form.get('town')
        data = {}
        key = '6d1cbcd7f1f15faea7b3accc84da2c51'
        url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'APPID': key, 'q': town, 'units': 'metric'}
        result = requests.get(url, params=params)
        weather = result.json()  # превратить ответ в формат json
        code = weather['cod']  # если города нет, поймать ошибку
        icon = weather['weather'][0]['icon']
        temp = int(weather['main']['temp'])
        vlag = weather['main']['humidity']
        data['code'] = code  # внесем в пустой словарь
        data['icon'] = icon
        data['temp'] = temp

        return render_template('weather.html', title=f'Погода в городе{town}', town=town, data=weather, icon=icon,
                               temp=temp, vlag=vlag)


@app.route('/var_test')
def var_test():
    return render_template('var_test.html', title='Определяем переменную внутри HTML')


@app.route('/odd_even')
def odd_even():
    return render_template('odd_even.html', number=3)


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    # with open('news.json', 'rt', encoding='utf-8') as f:
    #     news_list = json.loads(f.read())
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()  # ORM
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)  # слияние сессии с текущим пользователем
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости', form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html', title='Редактирование новости',
                           form=form)


@app.route('/news_del/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


# @app.route('/news')
# def news():
#     lst = ['ANN', 'TOM', 'BOB']
#     return render_template('news.html', title="FOR", news=lst)

@app.route('/slogan')
def slogan():
    return 'Ибо крепка, как смерть, любовь<br><a href="/">Назад</a> '


@app.route('/form_sample', methods=['GET', 'POST'])
def form_sample():
    if request.method == 'GET':
        return render_template('user_form.html', title="Форма")
    elif request.method == 'POST':
        f = request.files['file']
        f.save('./static/images/loaded.png')
        myform = request.form.to_dict()  # превратим в словарь
        return render_template('filled_form.html', title='Ваши данные', data=myform)


@app.route('/load_photo', methods=['GET', 'POST'])
def load_photo():
    if request.method == 'GET':
        return f"""
        
        <form class="login_form" method="post" enctype="multipart/form-data"> <!--отправка файлов -->
            <div class="form-group">
            <label for="photo">Приложите фото</label>
            <input type="file" class="form-control-file" id="photo" name="file">
            </div>
        <br>
        <button type="submit" class="btn btn-primary">Отправить</button>
        </form>
        """
    elif request.method == 'POST':
        f = request.files['file']  # если file нет, то будет исключение
        # request.form.get('file') - исключения не будет выброшено, лучше этот способ
        f.save('./static/images/loaded.png')
        return '<h1>Файл у вас на сервере</h1>'


@app.route('/mail', methods=['GET'])
def get_form():
    return render_template('mail_send.html')


@app.route('/mail', methods=['POST'])
def post_form():
    email = request.values.get('email')
    if send_mail(email, 'Вам письмо', 'Текст письма'):
        return f'Письмо на адрес {email} отправлено успешно!'
    return 'Сбой при отправке'


if __name__ == '__main__':
    db_session.global_init('db/news.sqlite')
    app.run(host='127.0.0.1', port=5000, debug=True)
    # db_sess = db_session.create_session()

    # вывести все новости пользователя
    # user = db_sess.query(User).filter(User.id == 1).first()
    # for user in user.news:
    #     print(user)

    # добавим новость по ид
    # id = db_sess.query(User).filter(User.id == 1).first()
    # print(id.id)
    # news = News(title="Новости от Владимира №2", content='Больше не опаздываю', user_id=id.id, is_private=False)
    # db_sess.add(news)
    # db_sess.commit()
    # u = db_sess.query(User).filter(User.id == 1).first()
    # news = News(title="Новости от Владимира №4", content='Пошел на обед', is_private=False)
    # u.news.append(news)
    # db_sess.commit()

    # user = db_sess.query(User).first()
    # print(user.name)

    # users = db_sess.query(User).all()
    # for user in users:
    # print(user.name, user.email)
    # print(user)  # метод __repr__
    #
    # users = db_sess.query(User).filter(User.email.notilike('%v%'))  # ilike - i не учитывает регистр
    # #  в запросе | - или  & - и
    # for user in users:
    #     print(user)

    # обновление
    # user = db_sess.query(User).filter(User.id == 1).first()
    # user.name ="Vladimir"
    # print(user.name)

    # удалим
    # user = db_sess.query(User).filter(User.id == 2).first()
    # db_sess.delete(user)
    # db_sess.commit()

#  создание пользователя в БД
# user = User()
# user.name = 'Markus'
# user.about = 'Plumber9'
# user.email = 'markus@mail.ru'
#
# db_sess.add(user)
# db_sess.commit()
