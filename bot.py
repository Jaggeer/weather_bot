import logging

from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN
from database  import Database
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import gismeteoParser

API = API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db = Database('db.db')

class Form(StatesGroup):
	city = State()
	update = State()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Используй комманду /help, чтобы увидеть мой список комманд!")


@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
	msg = ("Я могу ответить на следующие команды:\n/help - помощь\n/city - выбор города для новых пользователей"
			+"\n/update - смена города\n/getweather - погода на текущее время")
	await message.answer(msg)


@dp.message_handler(commands=['city'])
async def command_city(message: types.Message):
	msg = "Напишите город для отображения погоды."
	await message.answer(msg)
	await Form.city.set()


@dp.message_handler(state=Form.city)
async def command_set_city(message: types.Message, state: FSMContext):
	msg = message.text
	if(not db.user_exists(message.from_user.id)):
		db.set_city(message.from_user.id, msg)
		await message.answer("Ваши данные внесены!")
		await state.finish()
	else:
		await message.answer("Вы уже вносили свои данные.\nИспользуйте комманду /update, чтобы обновить город.")
		await state.finish()


@dp.message_handler(commands=['update'])
async def command_update(message: types.Message):
	msg = "Напишите на какой город вы хотите заменить текущий."
	await message.answer(msg)
	await Form.update.set()


@dp.message_handler(state=Form.update)
async def command_update_city(message: types.Message, state: FSMContext):
	msg = message.text
	if(not db.user_exists(message.from_user.id)):
		db.set_city(message.from_user.id, msg)
		await message.answer("Ваши данные внесены!")
		await state.finish()
	else:
		db.update_city(message.from_user.id, msg)
		await message.answer("Вы поменяли город.")
		await state.finish()


@dp.message_handler(commands=['getweather'])
async def command_getweather(message: types.Message):
	if(db.user_exists(message.from_user.id)):
		city = db.get_city(message.from_user.id)
		msg = gismeteoParser.parse(city)
		await message.answer(msg)
	else:
		await message.answer("Для начала выберете город.")


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)