import requests


class Hotels:
    def __init__(self) -> None:
        self.__headers = {
            "X-RapidAPI-Key": "5bafa34540msh145ec0d2cb36517p13be7ajsn0fdf84d81f8a",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}
        self.__sort_type = ['PRICE_LOW_TO_HIGH', 'PRICE_HIGH_TO_LOW']
        self.__region = dict()
        self.__utils_hash = dict()


    def set_cities_id(self, id:int, city:str) -> None:
        """
        Находит все подходящие регионы под название города где идёт поиск отеля и сохраняет их списком игнорируя регион RUS
        
        RUS регион игнорируеться так-как агрегатор не выдает информации по жтому региону
        """
        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q":city,"locale":"ru","langid":"1033","siteid":"300000001"}        
        response = requests.get(url, headers=self.__headers, params=querystring)

        for i_hotel in response.json()['sr']:
            if i_hotel['hierarchyInfo']['country']['isoCode3'] != 'RUS':
                try:
                    self.__region.update({id: str(i_hotel['gaiaId'])})
                    
                except:
                    continue
    

    def set_propereties_list(self, id:int, sort_bool: bool, city:str, arrival_year:int, arrival_month:int, arrival_day:int,
                             departure_year:int, departure_month:int, departure_day:int, guests:int, childs:list, min_price:int,
                             max_price:int) -> None:
        """
        подставляеться вся информация из hash.json для поиска конкретно по параметрам запроса.
        
        Обнуление индекса для срезания списка.
        """
        url = "https://hotels4.p.rapidapi.com/properties/v2/list"

        self.set_cities_id(id, city)
        payload = {
                    "currency": "USD",
                    "eapid": 1,
                    "locale": "en_US",
                    "siteId": 300000001,
                    "destination": { "regionId": self.__region[id]},
                    "checkInDate": {
                        "day": arrival_day,
                        "month": arrival_month,
                        "year": arrival_year},
                    
                    "checkOutDate": {
                        "day": departure_day,
                        "month": departure_month,
                        "year": departure_year},
                    
                    "rooms": [
                        {
                            "adults": guests,
                            "children": childs
                        }
                    ],

                    "resultsStartingIndex": 0,
                    "resultsSize": 200,
                    "sort": self.__sort_type[sort_bool],
                    "filters": { "price": {
                            "max": max_price,
                            "min": min_price
                        } }}

        local_headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "5bafa34540msh145ec0d2cb36517p13be7ajsn0fdf84d81f8a",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}
        
        response = requests.post(url, json= payload, headers= local_headers)

        self.collecting_responces(id, response.json())


    def collecting_responces(self, id:int, responce:dict):
        """
        Собирает из ответа с сервера нужные данные и формирует их в словарь
        """

        self.__utils_hash.update({id: dict()})
        self.__utils_hash[id].update({'hotels': list(), 'act_index': 0})
        for aux in responce['data']['propertySearch']['properties']:
            try:
                aux_dict = dict()
                aux_dict['hotel_name'] = aux['name']
                aux_dict['image_url'] = aux['propertyImage']['image']['url']
                aux_dict['miles'] = aux['destinationInfo']['distanceFromDestination']['value']
                aux_dict['amount'] = aux['price']['lead']['amount']
                aux_dict['reviews'] = aux['reviews']['score'],
                aux_dict['description_to_url'] = aux['propertyImage']['image']['description']
                    
                self.__utils_hash[id]['hotels'].append(aux_dict)
            except:
                continue



    def get_hotel_list(self, id:int, index:int) -> list[dict]:
        """
        возвращает список форматированных отелей
        """
        self.__utils_hash[id]['act_index'] += index
        aux = self.__utils_hash[id]['hotels'][self.__utils_hash[id]['act_index'] - 5:self.__utils_hash[id]['act_index']:]
        return aux