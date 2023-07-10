from flask import Flask, url_for, request

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return 'Адмирал<br> ' \
           '<a href="/coutdown">Отсчет</a><br> ' \
           '<a href="/slogan">Слоган </a>'

@app.route('/form_sample', methods=['GET','POST'])
def form_sample():
    if request.method == 'GET':
        return f"""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Форма</title>
                <link rel="stylesheet" type="text/css" href ="{url_for('static', filename='css/style.css')}">
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
            </head>
            <body>
            <h1>Форма для регистрации<h2>
            <div class="container">
            <form class="login_form" method="post">
            <input type="text" class="form-control" name="fname" placeholder="Фамилия"></br>
            <input type="text" class="form-control" name="sname" placeholder="Имя"></br>
            <input type="email" class="form-control" name="email" placeholder="E-mail"></br>
            <input type="password" class="form-control" name="password" placeholder="Password"></br>
            
            <div class = "form-group">
            <label for="classSelect">Ваше образование</label>
            <select class="form-control" id="classSelect" name="profession">
            <option>Среднее</option>
            <option>Высшее</option>
            </select>
            </div>
            <button type="submit" class="btn btn-primary">Отправить</button>
            
            </form>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-Fy6S3B9q64WdZWQUiU+q4/2Lc9npb8tCaSX9FK7E8HnRr0Jz8D6OP9dO5Vg3Q9ct" crossorigin="anonymous"></script>
            </body>
            </html>"""
    elif request == 'POST':
        print(request.form['fname'])
        print(request.form['sname'])
        return 'Форма отправлена'




@app.route('/slideshow')  # карусель
def slideshow():
    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Постер</title>
        <link rel="stylesheet" type="text/css" href ="{url_for('static', filename='css/style.css')}">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
    </head>
    <body>
    <h1 class="red">Карусель</h1>
  <div id="carouselExampleControls" class="carousel slide" data-ride="carousel">
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="{url_for('static', filename='images/1.jpg')}" class="d-block w-100" alt="Картинка 1">
    </div>
    <div class="carousel-item">
      <img src="{url_for('static', filename='images/2.jpg')}" class="d-block w-100" alt="Картинка 2">
    </div>
    <div class="carousel-item">
      <img src="{url_for('static', filename='images/3.jpg')}" class="d-block w-100" alt="Картинка 3">
    </div>
  </div>
 <button class="carousel-control-prev" type="button" data-target="#carouselExampleControls" data-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="sr-only">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-target="#carouselExampleControls" data-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="sr-only">Next</span>
  </button>
</div>

    <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-Fy6S3B9q64WdZWQUiU+q4/2Lc9npb8tCaSX9FK7E8HnRr0Jz8D6OP9dO5Vg3Q9ct" crossorigin="anonymous"></script>
    </body>
    </html>"""


@app.route('/slogan')
def slogan():
    return 'Ибо крепка, как смерть, любовь<br><a href="/">Назад</a> '


@app.route('/coutdown')
def coutdown():
    lst = [str(x) for x in range(10, 0, -1)]
    lst.append('Start!!!')
    return '<br>'.join(lst)


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


@app.route('/nekrasov/<username>')
def nekrasov(username):
    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{username}</title>
        <link rel="stylesheet" type="text/css" href ="{url_for('static', filename='css/style.css')}">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
    </head>
    <body>
    <h1 class="text-center">Стихи Некрасова, {username}</h1>
    <div class="p-3 mb-2 bg-info text-white container">
    <div class="row"> 
    <div class="col">
    <img src="{url_for('static', filename='images/nekrasov.jpg')}" class="rounded-circle" alt ="Здесь должна была быть картинка, но не нашлась" >
    </div>
    <div class="col">
    <p class="text-warning bg-dark text-center">Однажды, в студеную зимнюю пору,<br> Я из лесу вышел; был сильный мороз. <br>
    Гляжу, поднимается медленно в гору<br>Лошадка, везущая хворосту воз.</p>
    <p class="text-dark bg-success text-center">И, шествуя важно, в спокойствии чинном,<br> Лошадку ведет под уздцы мужичок<br> В больших сапогах, в полушубке овчинном,<br>
     В больших рукавицах… а сам с ноготок!</p>
     </div>
     </div></div>
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-Fy6S3B9q64WdZWQUiU+q4/2Lc9npb8tCaSX9FK7E8HnRr0Jz8D6OP9dO5Vg3Q9ct" crossorigin="anonymous"></script>
    </body>
    </html>"""


@app.route('/variants/<int:var>')  # по умолчанию str формат, поэтому int
def variants(var):
    if var == 1:
        return f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Постер</title>
            <link rel="stylesheet" type="text/css" href ="{url_for('static', filename='css/style.css')}">
        </head>
        <body>
            <dl>
            <dt>Пан или пропал</dt>
            <dd>А что</dd>
            </dl>
        
        <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-Fy6S3B9q64WdZWQUiU+q4/2Lc9npb8tCaSX9FK7E8HnRr0Jz8D6OP9dO5Vg3Q9ct" crossorigin="anonymous"></script>
        </body>
        </html>"""
    elif var == 2:
        return f"""<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Постер</title>
                    <link rel="stylesheet" type="text/css" href ="{url_for('static', filename='css/style.css')}">
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
                </head>
                <body>
                    <dl>
                    <dt>Даже если вас сьели, у Вас есть два</dt>
                    <dd>А что</dd>
                    <dd>А что</dd>
                    </dl>

                <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-Fy6S3B9q64WdZWQUiU+q4/2Lc9npb8tCaSX9FK7E8HnRr0Jz8D6OP9dO5Vg3Q9ct" crossorigin="anonymous"></script>
                </body>
                </html>"""
    else:
        return "Я не знаю о чем вы!"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
