import json
from datetime import date
from sql.database import User

class jData:
    def __init__(self, id: str) -> None:
        """
        Сохраняеться id пользователя для передачи в дальнейшем по функциям и запуск создания стола sqlalcemy
        """
        self.__user_id = id
        self.__user_actual_city = None
        self.__sql = User()


    def set_arrival_date(self,ar_date: str) -> None:
        """
        Задаеться дата прибытия в виде строки для передачи в шаблон запроса
        """
        with open('hash/hash.json') as r_hash:
            loaded_dict = json.load(r_hash)

            ar_date = ar_date.split('-')
            rec_dict = {'year':int(ar_date[0]),
                        'month': int(ar_date[1]),
                        'day': int(ar_date[2])}

            loaded_dict[self.__user_id]['arrival'] = rec_dict

        with open('hash/hash.json', 'w') as w_hash:
            json.dump(loaded_dict, w_hash, indent = 2)


    def set_departure_date(self,dep_date: str) -> None:
        """
        Задаеться дата вылета в виде строки для передачи в шаблон запроса
        """
        with open('hash/hash.json') as r_hash:
            loaded_dict = json.load(r_hash)

            dep_date = dep_date.split('-')
            rec_dict = {'year':int(dep_date[0]),
                        'month': int(dep_date[1]),
                        'day': int(dep_date[2])}

            loaded_dict[self.__user_id]['departure'] = rec_dict

        with open('hash/hash.json', 'w') as w_hash:
            json.dump(loaded_dict, w_hash, indent = 2)


    def set_guest_num(self, guests:int) -> None:
        """
        Задаеться колличество людей для прибытия
        """
        with open('hash/hash.json') as r_hash:
            loaded_dict = json.load(r_hash)
            loaded_dict[self.__user_id]['guest_num'] = guests

        with open('hash/hash.json', 'w') as w_hash:
            json.dump(loaded_dict, w_hash, indent = 2)


    def set_child_bool(self, child:bool) -> None:
        """
        Указываеться будут-ли дети среди гостей
        """
        with open('hash/hash.json') as r_hash:
            loaded_dict = json.load(r_hash)
            loaded_dict[self.__user_id]['child_bool'] = child

            if child == False:
                loaded_dict[self.__user_id]['childs'] = list()
                

        with open('hash/hash.json', 'w') as w_hash:
            json.dump(loaded_dict, w_hash, indent = 2)


    def set_childs_num(self, childs_num:int) -> None:
        """
        Задаеться колличество детей для шаблона 
        """
        with open('hash/hash.json') as r_hash:
            loaded_dict = json.load(r_hash)
            loaded_dict[self.__user_id]['childs'] = childs_num

        with open('hash/hash.json', 'w') as w_hash:
            json.dump(loaded_dict, w_hash, indent = 2)


    def set_childs_age(self, ages:str) -> None:
        """
        Задаеться возраст детей
        """

        with open('hash/hash.json') as r_hash:
            loaded_dict = json.load(r_hash)
            
            if len(ages) == 1:
                loaded_dict[self.__user_id]['childs_age'] = [{'age':int(ages)}]

            else:
                local_list = list()
                ages = ages.split(',')
                for index in range(int(loaded_dict[self.__user_id]['childs'])):
                    local_list.append({'age':int(ages[index])})
                
                loaded_dict[self.__user_id]['childs_age'] = local_list

        with open('hash/hash.json', 'w') as w_hash:
            json.dump(loaded_dict, w_hash, indent = 2)


    def set_user(self) -> None:
        """
        Задаеться пользователь
        """
        with open('hash/hash.json') as r_hash:
            loaded_dict = json.load(r_hash)
            loaded_dict.update({self.__user_id: None})

        with open('hash/hash.json', 'w') as w_hash:
            json.dump(loaded_dict, w_hash, indent = 2)


    def set_custom_price(self, custom_price:str) -> None:
        """
        Задача диапазона цен для шаблона 
        """
        with open('hash/hash.json') as r_hash:
            loaded_dict = json.load(r_hash)
            custom_price.split('-')
            loaded_dict[self.__user_id]['min'] = custom_price[0]
            loaded_dict[self.__user_id]['max'] = custom_price[1]

        with open('hash/hash.json', 'w') as w_hash:
            json.dump(loaded_dict, w_hash, indent = 2)


    def update_user_city(self, city: str) -> None:
        """
        Обновляеться город пользователя, задаються базовые цены для шаблона 
        """
        self.__user_actual_city = city
        self.__sql.set_user(self.__user_id, city)

        with open('hash/hash.json') as r_hash:
            loaded_dict = json.load(r_hash)
            loaded_dict.update({self.__user_id: {'act_city': city}})
            loaded_dict[self.__user_id]['min'] = 10
            loaded_dict[self.__user_id]['max'] = 10000
            loaded_dict[self.__user_id]['childs_age'] = list()

        with open('hash/hash.json', 'w') as w_hash:
            json.dump(loaded_dict, w_hash, indent = 2)


    def get_user_city(self) -> str:
        """
        Возвращает название города, сначала проверяет в hash.json, если там не находит то в Users_DataBase.sql
        """
        if self.__user_actual_city == None:
            with open('hash/hash.json') as hash:
                try:
                    return json.load(hash)[self.__user_id]['act_city']
                
                except:
                    return self.__sql.get_user_city_sql(self.__user_id)
        else:
            return self.__user_actual_city


    def check_user(self) -> bool:
        """
        Проверяет новый-ли пользователь использует бота при команде /start если не находит в hash.json, то изет в Users_DataBase.sql
        """

        with open('hash/hash.json') as hash:
            try:
                json.load(hash)[self.__user_id]
                return True
            
            except:
                if self.__sql.check(self.__user_id):
                    return True
                
                else:
                    return False


    def aux_get_history(self) -> list():
        """
        Возвращает список запросов городов из Users_DataBase.sql

        не сделано на прямую что-бы не делать лишний импорт в handlers 
        """
        return self.__sql.get_history(self.__user_id)