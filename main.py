#Установить aiogram и requests библиотеки для работы с Telegram API и публичными API.
pip install aiogram requests
#Получить токен для доступа к Telegram Bot API, зарегистрировав нового бота через @BotFather.
#Создать модуль bot.py для реализации бота и подключить необходимые модули.
import os
import aiohttp
from forex_python.converter import CurrencyRates
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, InputMediaPhoto
from aiogram.utils import executor
import random
#Загрузить переменные окружения из файла .env.
TOKEN = os.environ.get('BOT_TOKEN') # токен доступа к боту
#Создать экземпляр бота и диспетчера для обработки входящих сообщений и команд.
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
#Создать функцию приветствия пользователя и предложения выбрать определенную функцию бота
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """
    Отправляет сообщение со списком доступных команд.
    """
    await message.reply("Привет! Я могу помочь вам с погодой, валютой, картинками и опросами. "
                        "Выберите одну из доступных команд: /weather, /currency, /picture, /poll")

#Создать функцию определения текущей погоды в определенном городе с использованием публичного API погоды и выдачи пользователю соответствующей информации.
async def get_weather(message: types.Message):
    """
    Получает текущую погоду в указанном городе с помощью API OpenWeatherMap и отправляет результат пользователю.
    """
    city = message.text.split()[1]
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=your_api_key&units=metric'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    if data['cod'] != 200:
        await message.reply("Я не могу найти такой город. Пожалуйста, попробуйте снова.")
    else:
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        description = data['weather'][0]['description']
        await message.reply(f"Текущая температура в городе {city}: {temp}°C, ощущается как {feels_like}°C.\n{description.capitalize()}")

    # Обработчик команды /currency
    @dp.message_handler(commands=['currency'])
    async def convert_currency(message: types.Message):
        """
        Конвертирует указанную сумму из одной валюты в другую с помощью API Exchange Rates и отправляет результат пользователю.
        """
        try:
            amount, from_currency, to_currency = message.text.split()[1:]
            amount = float(amount)
        except ValueError:
            await message.reply("Неверный формат команды. Пожалуйста, введите сумму и валюты через пробел.")
            return

        c = Currency