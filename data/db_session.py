#  Создание базы данных и сессии по работе с ней
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = orm.declarative_base()

created = None  # создана ли сессия


def global_init(db_file):
    global created

    if created:
        return
    if not db_file or not db_file.strip():  # очищаем пробелы
        raise Exception("Забыли подключить файл базы!")
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False '  # не используем тот же поток данных false
    print(f'мы подключились к базе: {conn_str}')
    engine = sa.create_engine(conn_str, echo=False)  # движок
    created = orm.sessionmaker(bind=engine)
    from . import all_models
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:  # аннотатор функций, возвращает сессию
    global created
    return created()
