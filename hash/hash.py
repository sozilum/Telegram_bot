from utils.hotels import Hotels


class Hash:
    def __init__(self) -> None:
        self.__booking = Hotels()
        self.__booking.env_init()
        self.__users = dict()


    def check(self, id:int) -> bool:
        """
        Проверяет есть-ли id пользователя в словаре и если есть, то возвращает True, в противном случае добавляет в словарь
        id пользователя и возвращает False 
        """
        if id in self.__users:
            return True
        
        else:
            return False
        

    def get_user_city(self, id:int) -> str:
        """
        Возвращает название города пользователя
        """
        return self.__users[id]['city']


    def set_user_city(self, id:int, city_name:str) -> None:
        """
        Добавляет город пользователя в словарь, по id пользователя и добавляет город пользователя в список истории запросов
        """
        self.__users.update({id: dict()})
        self.__users[id].update({'city': city_name, 'history': list(),'min': 10, 'max': 1000,  'childs_age': []})
        self.__users[id]['history'].append(city_name)
        

    def set_user_arrival(self, id:int, arrival_date:str) -> None:
        """
        Добавляет дату прибытия пользователя в словарь, по id пользователя
        """
        aux_list = [int(date) for date in arrival_date.split('-')]

        self.__users[id].update({'arrival_year': aux_list[0], 'arrival_month': aux_list[1], 'arrival_day': aux_list[2]})


    def set_user_departure(self, id:int, departure_date:str) -> None:
        """
        Добавляет дату убытия пользователя в словарь, по id пользователя 
        """
        aux_list = [int(date) for date in departure_date.split('-')]

        self.__users[id].update({'departure_year': aux_list[0], 'departure_month': aux_list[1], 'departure_day': aux_list[2]})


    def set_user_guests(self, id:int, guests_num:int) -> None:
        """
        Добавляет колличество гостей в словарь, по id пользователя
        """

        self.__users[id].update({'guests': guests_num})


    def set_childs_num(self, id:int, childs_num:str) -> None:
        """
        Добавляет колличетсво детей в словарь, по id пользователя 
        """

        self.__users[id].update({'childs': childs_num})


    def set_childs_age(self, id:int, childs_age:str) -> None:
        """
        Добавляет возраст детей в словарь, по id пользователя
        """

        self.__users[id].update({'childs_age': [{'age': int(age)} for age in childs_age.split(',')]})


    def set_custom_price(self, id:int, price:str) -> None:
        """
        Добавляет пользовательскую цену в словарь, по id пользователя 
        """
        min_price, max_price = price.split('-')

        self.__users[id].update({'min': int(min_price), 'max': int(max_price)})


    def get_hotel_list(self, id:int, index:int = 5) -> dict:
        return self.__booking.get_hotel_list(id, index)

    
    def set_propereties_list(self, id:int, sort_type:bool = False) -> None:
        self.__booking.set_propereties_list(id, sort_type, self.__users[id]['city'], self.__users[id]['arrival_year'], self.__users[id]['arrival_month'],
                                            self.__users[id]['arrival_day'], self.__users[id]['departure_year'], self.__users[id]['departure_month'],
                                            self.__users[id]['departure_day'], self.__users[id]['guests'], self.__users[id]['childs_age'],
                                            self.__users[id]['min'], self.__users[id]['max'])


    def get_history(self, id:int) -> list:
        """
        Возвращает история запросов городов пользователя
        """

        return self.__users[id]['history']