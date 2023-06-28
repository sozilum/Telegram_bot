from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped,Session ,mapped_column


class Base(DeclarativeBase): pass
"""
class Base - Базовые параметры создания стола дял sql
"""
class User_table(Base):
    """
    Создание стола для users_database
    """
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(primary_key= True)
    user_id: Mapped[str] = mapped_column(String(30))
    city_name: Mapped[str] = mapped_column(String(1000))


class User:
    def __init__(self) -> None:
        """
        Запуск двигателя и создание сессии sqlalchemy
        """
        self.__engine = create_engine('sqlite:///sql/users_database.sql', echo = True)
        self._meta = Base.metadata.create_all(self.__engine)
        self.__session = Session(self.__engine)


    def set_user(self, id: str = None, city_name: str = None) -> None:
        """
        Записать пользователя и города в базу данных
        """

        with self.__session as session:
            user = User_table(
                user_id = '{}'.format(id),
                city_name = '{}'.format(city_name),
        )
        
        session.add(user)
        session.commit()


    def update_city_name(self, id:str = None, new_city:str = None):
        """
        Обновить название города где происходит поиск апартаментов 
        """
        update_city = select(User_table).where(User_table.user_id.in_([id]))
        city = self.__session.scalars(update_city).one()
        city.city_name.replace(new_city)
        self.__session.commit()


    def get_user_city_sql(self, id:str = None) -> str:
        """
        Возвращает последний созраненный город в sql
        """
        request = select(User_table).where(User_table.user_id.in_([id]))
        
        for city in self.__session.scalars(request):
            return city.city_name


    def check(self, id:str = None) -> bool:
        """
        Проверка наличия пользователя в базе данных
        """

        check_user = select(User_table).where(User_table.user_id.in_([id]))
        
        for i_check in self.__session.scalars(check_user):
            if i_check:
                
                return True
            
    def get_history(self, id:str) -> list:
        """
        Возвращает историю городов
        """
        history_list = select(User_table).where(User_table.user_id.in_([id]))
        local_list = list()
        
        for city in self.__session.scalars(history_list):
            local_list.append(city.city_name)

        return local_list