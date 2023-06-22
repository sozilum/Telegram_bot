import json
import requests


class Hotels:
    def __init__(self) -> None:
        self.__headers = {
            "X-RapidAPI-Key": "5bafa34540msh145ec0d2cb36517p13be7ajsn0fdf84d81f8a",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}
        self.__sort_type = ['PRICE_LOW_TO_HIGH', 'PRICE_HIGH_TO_LOW']
        self.__region_list_id = list()


    def set_cities_list_id(self, city:str) -> None:
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
                    self.__region_list_id.append(str(i_hotel['gaiaId']))
                
                except:
                    continue
    
    def set_propereties_list(self, act_user:str, sort_bool: bool = False, i_region_id:int = 0) -> None:
        """
        подставляеться вся информация из hash.json для поиска конкретно по параметрам запроса.
        
        Обнуление индекса для срезания списка.
        """
        url = "https://hotels4.p.rapidapi.com/properties/v2/list"
        #Здесть почему-то прихолдит ответ по старому запросу, помогает только перезапуск бота 
        with open('Hash/hash.json') as file:
            jfile = json.load(file)
            user = jfile[act_user]
            self.set_cities_list_id(user['act_city'])
            user['act_index'] = 0
            payload = {
                        "currency": "USD",
                        "eapid": 1,
                        "locale": "en_US",
                        "siteId": 300000001,
                        "destination": { "regionId": self.__region_list_id[i_region_id]},
                        "checkInDate": {
                            "day": user['arrival']['day'],
                            "month": user['arrival']['month'],
                            "year": user['arrival']['year']},
                        
                        "checkOutDate": {
                            "day": user['departure']['day'],
                            "month": user['departure']['month'],
                            "year": user['departure']['year']},
                        
                        "rooms": [
                            {
                                "adults": user['guest_num'],
                                "children":user['childs_age']
                            }
                        ],

                        "resultsStartingIndex": 0,
                        "resultsSize": 100,
                        "sort": self.__sort_type[sort_bool],
                        "filters": { "price": {
                                "max": user['max'],
                                "min": user['min']
                            } }}


        local_headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "5bafa34540msh145ec0d2cb36517p13be7ajsn0fdf84d81f8a",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}

        response = requests.post(url, json= payload, headers= local_headers)
        self.formating_hotels_list(response.json(), act_user)
            

    def formating_hotels_list(self, json_response, act_user:str) -> None:
        """
        Отсеивание всех ненужных данных (Приходит слишком много)
        """
        hotel_list = json_response['data']['propertySearch']['properties']
        
        with open('Hash/hotels_hash.json') as jfile:
            user = json.load(jfile)

            user[act_user] = {'hotels': list()}    

            for i_hotel in hotel_list:
                aux_dict = dict()
                aux_dict['hotel_name'] = i_hotel['name']
                aux_dict['image_url'] = i_hotel['propertyImage']['image']['url']
                aux_dict['miles'] = i_hotel['destinationInfo']['distanceFromDestination']['value']
                aux_dict['amount'] = i_hotel['price']['lead']['amount']
                aux_dict['reviews'] = i_hotel['reviews']['score'],
                aux_dict['description_to_url'] = i_hotel['propertyImage']['image']['description']
                    
                user[act_user]['hotels'].append(aux_dict)
            user[act_user].update({'act_index': 0})

        with open('Hash/hotels_hash.json', 'w') as file:
            json.dump(user, file, indent= 2)


    def get_hotel_list(self, act_user:str, index: int = 5) -> list[dict]:
        """
        возвращает список форматированных отелей
        """
        with open('Hash/hotels_hash.json') as file:
            user = json.load(file)
            user[act_user]['act_index'] += index
            aux = user[act_user]['hotels'][user[act_user]['act_index'] - 5:user[act_user]['act_index']:]
        
        with open('Hash/hotels_hash.json', 'w') as file:
            user = json.dump(user, file, indent= 2)

        return aux
