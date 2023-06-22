from aiogram import types

class Buttons:
    def main_button(self) -> list[list]:
        """
        main_button - кнопки основного меню ¯\_(ツ)_/¯
        """
        keyboard_list= [
            [types.KeyboardButton(text = 'Указать город')],
            [types.KeyboardButton(text = 'Цены по возрастанию')],
            [types.KeyboardButton(text = 'Цены по убыванию')],
            [types.KeyboardButton(text = 'Задать диапозон цен')],
            [types.KeyboardButton(text = 'Историю просмотров')]
        ]
        return keyboard_list
