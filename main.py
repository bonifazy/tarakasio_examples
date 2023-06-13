from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Глобальные переменные обычно принято называть константами.
# Константы в Питоне обычно пишут капслоком, потом в коде проще понять откуда идет эта переменная
# (ниже в коде понятно, что ее надо искать где- то тут в начале кода)
NAME = ''


@dp.message_handler(commands=['start'])
async def start_menu(msg: types.Message):
    start_markup = [[types.KeyboardButton(text="/start")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=start_markup)
    # Если имя пустое, то запросить актуальное имя юзера
    if not NAME:
        await msg.answer(f'Привет, {msg.from_user.first_name}! \n\n/start - Основное меню \n/help - Помощь \n\n'
                         f'Введите Ваше актуальное полное имя: ', reply_markup=keyboard)
    # Имя найдено, использовать именно его
    else:
        await msg.answer(f'Привет, {NAME}! \nВаше имя из Telegram профиля: {msg.from_user.first_name}.\n\n'
                         'Любое новое введенное имя уже не изменит константу NAME. \n'
                         'Если нужно, чтобы имя перезаписывалось на новое, '
                         'достаточно поменять логику только функции get_name, не затрагивая остальной код проекта.')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    # Неверная логика кода, относительно идеи хендлера (относительно текста)
    await message.reply("Напиши что- нибудь и я отправлю этот текст в ответ! \n\n"
                        "UPD. Хендлер не будет обрабатываться, как по идее он был придуман, "
                        "т.к. его перехватывает echo_message запросом имени. Если нужно ждать ответ и на этот хендлер, "
                        "то надо писать дополнительный обрабочик.")


# Изначально твой пустой хендлер принимал абсолютно всё от юзера: и текст, и фотку, и файл и геолокацию.
# Нам нужен только текст, добавляем фильтр текста
# @dp.message_handler()
@dp.message_handler(content_types=['text'])
async def echo_message(msg: types.Message):

    # Если функция очень сильно зависит от echo_message и ее больше никто не вызывает,
    # то ее логичнее определить внутри самой echo_message, а не в глобальной области определения всех функций
    # (т.к. её стек памяти больше нахуй никому не нужен, кроме как функции echo_message)
    def get_name(name_from_user: str) -> str:
        global NAME
        if NAME == '':
            NAME = name_from_user
            return NAME
        else:
            return NAME

    # Вся логика поиска, записи и проверки имени в переменной обрабатывается только одной функцией get_name.
    # Пусть она всё и делает, т.к. возможно требуется еще доп обработка и неохота раздувать основной код.
    # Нам по итогу нужно только результат поиска имени, его и ожидаем
    name = get_name(msg.text)

    # если результат есть, то вывести его (вывести имя)
    if name:
        await bot.send_message(msg.from_user.id, f'Ваше имя: {name}\n\nОсновное меню: /start',
                               reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp)
