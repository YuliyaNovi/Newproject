from flask import Flask, url_for, request, redirect
from flask import render_template
import json
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
#    user = "Слушатель"
    param = {}
    param['username'] = 'Слушатель'
    param['title'] = 'Работа с шаблонами'
    return render_template('index.html', **param)  # * список **словарь
#  return render_template('index.html', title='Работа с шаблонами', username=user)

#  return redirect('/load_photo')  # безусловный редирект, сразу кидает пользователя на страницу с главной

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
        with open('./templates/user_form.html', 'r', encoding='utf-8') as html_stream:
            return html_stream.read()
    elif request.method == 'POST':
        print(request.form['fname'])
        print(request.form['sname'])
        return 'Форма отправлена'


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
    app.run(host='127.0.0.1', port=5000, debug=True)
