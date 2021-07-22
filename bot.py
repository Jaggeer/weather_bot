import logging

from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN

API = API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm WeatherBot!\nI'll send you weather in your city.")

@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
	msg = ("My commands:\n/start - welcome message\n/help - list of commands\n/city - select your city\n/update -"
			+ " update your city\n/getweather -"
			+ " get weather in your sity\n")
	await message.reply(msg)

@dp.message_handler(commands=['city'])
async def command_city(message: types.Message):


@dp.message_handler(commands=['update'])
async def command_update(message: types.Message):


@dp.message_handler(commands=['getweather'])
async def command_getweather(message: types.Message):


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)