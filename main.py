from flask import Flask, url_for, request, redirect
from flask import render_template
import json
import requests
from loginform import LoginForm
from data import db_session
from data.users import User
from data.news import News

app = Flask(__name__)
app.config['SECRET_KEY'] = 'too short key'
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///db/news.sqlite'


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template('index.html', title='Новости', news=news)  # * список **словарь


#  return render_template('index.html', title='Работа с шаблонами', username=user)

#  return redirect('/load_photo')  # безусловный редирект, сразу кидает пользователя на страницу с главной
@app.errorhandler(404)
def http_404_error(error):
    return redirect('/error404')


@app.route('/error404')
def well():  # колодец
    return render_template('well.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


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


@app.route('/news')
def news():
    with open('news.json', 'rt', encoding='utf-8') as f:
        news_list = json.loads(f.read())
    return render_template('news.html', title='Новости', news=news_list)


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


@app.route('/poster')
def poster():
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Постер</title>
    <link rel="stylesheet" type="text/css" href ="{url_for('static', filename='css/style.css')}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
</head>
<body>
<h1 class="red">Постер к фильму</h1>
<img src="{url_for('static', filename='images/admiral.jpeg')}" alt ="Здесь должна была быть картинка, но не нашлась" >
<p>И крепка, как смерть, любовь!</p>

<script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-Fy6S3B9q64WdZWQUiU+q4/2Lc9npb8tCaSX9FK7E8HnRr0Jz8D6OP9dO5Vg3Q9ct" crossorigin="anonymous"></script>
</body>
</html>"""


if __name__ == '__main__':
    db_session.global_init('db/news.sqlite')
    app.run(host='127.0.0.1', port=5000, debug=True)
    #db_sess = db_session.create_session()

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
