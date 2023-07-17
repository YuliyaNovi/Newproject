import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from sqlalchemy_serializer import SerializerMixin

# роль пользователя
# ACCESS {
#     'user': 1,
#     'admin': 2
#  }
class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    # level = sqlalchemy.Column(sqlalchemy.Integer, default=1)  # для назначение прав, нужно создать бд заново
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    news = orm.relationship("News", back_populates='user')  # связываем с классом и user

    def __repr__(self):
        return f'{self.name}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

# проверяем является ли пользователь админом
# def is_admin(self):
#     return self.level == ACCESS['admin']

# разрешение действий пользователю с текущим уровнем
# def allowed(self, access_level):
#     return self.level >= access_level
