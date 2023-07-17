from requests import get, post, delete

# Печатать в консоль, тестируем API get
# print(get('http://127.0.0.1:5000/api/v2/news/3').json())
# print(get('http://127.0.0.1:5000/api/v2/news/33').json())
# print(get('http://127.0.0.1:5000/api/v2/news/q').json())

# Печатать в консоль, тестируем API post
# print(post('http://127.0.0.1:5000/api/v2/news', json='').json())


new_rl = {'title': 'Заголовок API',
          'content': 'Новость Api',
          'user_id': 1,
          'is_private': False,
          'is_published': False
          }

print(post('http://127.0.0.1:5000/api/v2/news', json=new_rl).json())
# print(delete('http://127.0.0.1:5000/api/v2/news/21').json())
# print(delete('http://127.0.0.1:5000/api/v2/news/5').json())


