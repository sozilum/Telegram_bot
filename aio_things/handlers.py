import re
from utils.Hotels import Hotels
from Hash.jdata import jData
from aiogram import types, Router
from aiogram.types import Message, CallbackQuery
from aio_things.buttons import Buttons
from aiogram.utils.markdown import hlink
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()
buttons = Buttons()
booking = Hotels()

class Form(StatesGroup):
    """
    Шаблон запрашиваемых данных для машины состояний
    """
    city = State()
    arrival_date = State()
    departure_date = State()
    guests_num = State()
    childs_presence = State()
    childs_num = State()
    childs_age = State()
    custom_price = State()

@router.message(Command(commands = 'start'))
async def main(message: Message) -> Message:
    """
    user - Создание класса с id пользователя

    Первичный запуск бота и проверка пользователя в базе данных, если пользователь не найден в базе данных,
    то сразу предложит ввести город

    """

    user = jData(str(message.from_user.id))
    check_result = user.check_user()

    
    if check_result:
        kb = types.ReplyKeyboardMarkup(keyboard = buttons.main_button(), resize_keyboard = True, input_field_placeholder = 'Выберите действие')
        await message.answer('Здравствуйте!\nУ вас указан город {}'.format(user.get_user_city()),
                            reply_markup = kb)

    else:
        user.set_user()
        keyboard_list = [
            [types.KeyboardButton(text = 'Указать город')]
            ]
        kb = types.ReplyKeyboardMarkup(keyboard = keyboard_list, resize_keyboard = True, input_field_placeholder = 'Выберите действие')
        await message.answer('Здравствуйт!\nЭто телеграмм бот который поможет вам подобрать апартаменты в указаном вами населённом пункте!\nВ данный момент к сожалению бот не работает с Российскими городами.', 
                            reply_markup = kb)


@router.message(Text(text = 'Указать город'))
async def citychoice(message: Message, state: FSMContext) -> Message:

    """
    state.set_state(From.city) - Запуски машины проверки статуса пользователя.
    
    Form.city - запрос по шаблону для машины статуса
    """
    await state.set_state(Form.city)
    await message.answer('Введите населённый пункт где будем искать апартаменты: ')


@router.message(Form.city)
async def citychoice(message: Message, state: FSMContext) -> Message:

    """
    Запуск машины автоматов и указание города 

    state.update_data(name = message.text) - обновление машины статуса. name = message.text - Отлов сообщения для машины статуса

    """

    await state.update_data(name = message.text)
    user = jData(str(message.from_user.id))
    user.update_user_city(message.text)
    await state.set_state(Form.arrival_date)
    await message.answer('У вас указан город {}\nВведите дату прибытия в формате\nГод-месяц-день '.format(message.text))
    

@router.message(Form.arrival_date)
async def arrival_date(message: Message, state: FSMContext) -> Message:
    """
    Указание даты прибытия и передача в базу данных, для дальнейшей подстановки в шаблон
    """

    await state.update_data(name = message.text)
    user = jData(str(message.from_user.id))
    if re.fullmatch('\d{4}-\d{2}-\d{2}', message.text):
        user.set_arrival_date(message.text)
        await state.set_state(Form.departure_date)
        await message.answer('Ваша дата прибытия {}\nВведите дату вылета в формате\nГод-месяц-день'.format(message.text))
    
    else:
        await state.set_state(Form.arrival_date)
        await message.answer('дата введена в неверном формате, попробуйте ещё раз.\nВведите дату вылета в формате\nПример: 2023-05-12')


@router.message(Form.departure_date)
async def depart_date(message: Message, state: FSMContext) -> Message:
    """
    Указание даты убытия и передача в базу данных, для дальнейшей подстановки в шаблон
    """

    await state.update_data(name = message.text)
    user = jData(str(message.from_user.id))
    if re.fullmatch('\d{4}-\d{2}-\d{2}', message.text):
        user.set_departure_date(message.text)
        await state.set_state(Form.guests_num)
        await message.answer('Ваша дата вылета {}\nВведите колличество человек:'.format(message.text))
    
    else:
        await state.set_state(Form.departure_date)
        await message.answer('дата введена в неверном формате, попробуйте ещё раз.\nВведите дату вылета в формате\nПример: 2023-05-12')


@router.message(Form.guests_num)
async def guest_num(message: Message, state: FSMContext) -> Message:
    """
    Указание колличества гостей и передача в базу данных, для дальнейшей подстановки в шаблон
    """

    await state.update_data(name = message.text)
    user = jData(str(message.from_user.id))
    user.set_guest_num(int(message.text))
    if int(message.text) == 1:
        kb = types.ReplyKeyboardMarkup(keyboard = buttons.main_button(), resize_keyboard = True, input_field_placeholder = 'Выберите действие')
        await message.answer('Параметры введены, выберите способо фильтрации', reply_markup= kb)
        user.set_child_bool(False)
        await state.clear()

    
    else:
        await state.set_state(Form.childs_presence)
        await message.answer('Колличество людей: {}\nБудут ли дети:\nДа/Нет'.format(message.text))


@router.message(Form.childs_presence)
async def childs_bool(message: Message, state: FSMContext) -> Message:
    """
    Указание есть-ли среди гостей дети, для дальнейшей подстановки в шаблон
    
    Если ранее было указано что гость 1, то запрос на наличие детей не сработает 

    state.clear() - очистит машину автоматов после запроса всех необходимых данных для поиска  
    """

    await state.update_data(name = message.text)
    user = jData(str(message.from_user.id))
    if str(message.text).lower() == 'да':
        user.set_child_bool(True)
        await state.set_state(Form.childs_num)
        await message.answer('Введите Колличетсво детей: ')

    else:
        user.set_child_bool(False)
        await message.answer('Параметры введены, выберите из меню способ фильтраци')
        await state.clear()


@router.message(Form.childs_num)
async def childs_nums(message: Message, state: FSMContext) -> Message:
    """
    Указание колличества детей среди гостей 

    """
    await state.update_data(name = message.text)
    user = jData(str(message.from_user.id))
    user.set_childs_num(message.text)
    await state.set_state(Form.childs_age)
    await message.answer('Колличество детей: {}\nВведите возраст детей через запятую: '.format(message.text))


@router.message(Form.childs_age)
async def childs_ages(message: Message, state: FSMContext) -> Message:
    """
    Указание возраста детей 
    """
    
    await state.update_data(name = message.text)
    user = jData(str(message.from_user.id))
    user.set_childs_age(message.text)
    await message.answer('Параметры указаны, выберите из меню способ фильтрации')
    await state.clear()


@router.message(Text(text = 'Цены по возрастанию'))
async def apart_price_low(message: Message) -> Message:
    """
    Вывод апартаментов с фильтрацией от самых дорогих до самых дешёвых

    """
    booking.set_propereties_list(str(message.from_user.id))
    hotel_list = booking.get_hotel_list(act_user= str(message.from_user.id))
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(text = '<', callback_data=  'previous_page'),
        types.InlineKeyboardButton(text = '>', callback_data = 'next_page')
    )
    for i_hotel in hotel_list:
        link = hlink(i_hotel['description_to_url'], i_hotel['image_url'])
        await message.answer('{}\nНазвание отеля: {}\nЦена за ночь: {}$\nСредний рейтинг отзывов: {}\nКол-во миль от выбранного вами места: {}'.format(
            link,
            i_hotel['hotel_name'],
            i_hotel['amount'],
            i_hotel['reviews'],
            i_hotel['miles']
        ))
    await message.answer('Выберите действие',reply_markup= kb.as_markup(resize_keyboard = True))



@router.message(Text(text = 'Цены по убыванию'))
async def apart_price_hight(message: Message) -> Message:
    """
    Вывод апартаментов с фильтрацией от самых дорогих к самым дешёвым
    """
    booking.set_propereties_list(str(message.from_user.id), sort_bool= True)
    hotel_list = booking.get_hotel_list(act_user= str(message.from_user.id))
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(text = '<', callback_data=  'previous_page'),
        types.InlineKeyboardButton(text = '>', callback_data = 'next_page')
    )
    for i_hotel in hotel_list:
        link = hlink(i_hotel['description_to_url'], i_hotel['image_url'])
        await message.answer('{}\nНазвание отеля: {}\nЦена за ночь: {}$\nСредний рейтинг отзывов: {}\nКол-во миль от выбранного вами места: {}'.format(
            link,
            i_hotel['hotel_name'],
            i_hotel['amount'],
            i_hotel['reviews'],
            i_hotel['miles']
        ))
    await message.answer('Выберите действие',reply_markup= kb.as_markup(resize_keyboard = True))



@router.message(Text(text = 'Задать диапозон цен'))
async def custom_price_apart(message: Message, state: FSMContext) -> Message:
    """
    Указание диапазона цен для шаблона и запуск машины автоматов для получения цены 

    """
    await state.set_state(Form.custom_price)
    await message.answer('Введите какой диапазон цен,\nкоторый вас интересует через через -:\nmin - max')


@router.message(Form.custom_price)
async def request_custom_aparts(message: Message, state: FSMContext) -> Message:
    """
    Вывод от дешёвых к дорогим отлей, в заданном диапазоне
    """
    await state.update_data(name = message.text)
    
    if re.fullmatch('\d+-\d+', message.text):
        user = jData(str(message.from_user.id))
        user.set_custom_price(message.text)
        await state.clear()
        
        hotel_list = booking.get_hotel_list(act_user= str(message.from_user.id))
        kb = InlineKeyboardBuilder()
        kb.row(
        types.InlineKeyboardButton(text = '<', callback_data=  'previous_page'),
        types.InlineKeyboardButton(text = '>', callback_data = 'next_page')
        )
        
        for i_hotel in hotel_list:
            link = hlink(i_hotel['description_to_url'], i_hotel['image_url'])
            await message.answer('{}\nНазвание отеля: {}\nЦена за ночь: {}$\nСредний рейтинг отзывов: {}\nКол-во миль от выбранного вами места: {}'.format(
                link,
                i_hotel['hotel_name'],
                i_hotel['amount'],
                i_hotel['reviews'],
                i_hotel['miles']
            ))
        await message.answer('Выберите действие',reply_markup= kb.as_markup(resize_keyboard = True))

    else:
        await state.set_state(Form.custom_price)
        await message.answer('Введите пожалуйста диапазон цен согласно формату\nПример: 150-240')


@router.callback_query(Text(text = 'previous_page'))
async def previous_page(callback: CallbackQuery) -> Message:
    """
    Создаються кнопки при нажатии на которые передаеться отрицательны индекс для срезания списка и возврата 
    """
    hotel_list = booking.get_hotel_list(act_user= str(callback.from_user.id), index= -5)
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(text = '<', callback_data=  'previous_page'),
        types.InlineKeyboardButton(text = '>', callback_data = 'next_page')
    )
    for i_hotel in hotel_list:
        link = hlink(i_hotel['description_to_url'], i_hotel['image_url'])
        await callback.message.answer('{}\nНазвание отеля: {}\n Цена за ночь: {}$\n Средний рейтинг отзывов: {}\nКол-во миль от выбранного вами места: {}'.format(
            link,
            i_hotel['hotel_name'],
            i_hotel['amount'],
            i_hotel['reviews'],
            i_hotel['miles']
        ))
    await callback.message.answer('Выберите действие', reply_markup= kb.as_markup(resize_keyboard = True))


@router.callback_query(Text(text = 'next_page'))
async def next_page(callback: CallbackQuery) -> Message:
    """
    Создаються кнопки при нажатии на которые передаеться индекс для срезания списка и возврата 
    """
    hotel_list = booking.get_hotel_list(act_user= str(callback.from_user.id))
    kb = InlineKeyboardBuilder()
    kb.row(
        types.InlineKeyboardButton(text = '<', callback_data=  'previous_page'),
        types.InlineKeyboardButton(text = '>', callback_data = 'next_page')
    )
    for i_hotel in hotel_list:
        link = hlink(i_hotel['description_to_url'], i_hotel['image_url'])
        await callback.message.answer('{}\nНазвание отеля: {}\n Цена за ночь: {}$\n Средний рейтинг отзывов: {}\nКол-во миль от выбранного вами места: {}'.format(
            link,
            i_hotel['hotel_name'],
            i_hotel['amount'],
            i_hotel['reviews'],
            i_hotel['miles']
        ))
    await callback.message.answer('Выберите действие', reply_markup= kb.as_markup(resize_keyboard = True))


@router.message(Text(text = 'Историю просмотров'))
async def apart_history(message: Message) -> Message:
    """
    Вывод списка городов которые ранее запрашивал пользователь
    """
    user = jData(str(message.from_user.id))
    history_list = user.aux_get_history()
    await message.answer('Вот история запросов городов: ')

    for i_city in history_list:
        await message.answer('{}'.format(i_city))