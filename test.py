from requests import get, post, delete

# Печатать в консоль, тестируем API get
# print(get('http://127.0.0.1:5000/api/news/3').json())
# print(get('http://127.0.0.1:5000/api/news/33').json())
# print(get('http://127.0.0.1:5000/api/news/q').json())

# Печатать в консоль, тестируем API post
# print(post('http://127.0.0.1:5000/api/news').json())


# new_rl = {'title': 'Заголовок API',
#           'content': 'Новость Api',
#           'user_id': 1,
#           'is_private': False
#           }
#
# print(post('http://127.0.0.1:5000/api/news', json=new_rl).json())
# print(delete('http://127.0.0.1:5000/api/news/21').json())
# print(delete('http://127.0.0.1:5000/api/news/5').json())


