from aiogram import Dispatcher, types
from create import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import database.sqlite_db as db 
from keyboards.client import *
from keyboards.admin import *
import random

msg_id = {}

class RegisterFSM(StatesGroup):
    telegram_id = State()
    Name = State()
    Surname =State()
    Email = State()

async def task():
    try: 
        kb = None
        users = db.get_inf('Users')
        question = random.choice(db.get_inf('Questions', 'Used', False))
        global score
        score = question[6]
        await db.set_used(question[0])
        if msg_id:
            for user, message in msg_id.items():
                await bot.edit_message_reply_markup(user,message,reply_markup=None)
        for user in users:
            if question[-2]!=0:
                msg = await bot.send_photo(user[0], question[-2], question[1], reply_markup=inlinekeyboard((question[2], 'Right'),(question[3], 'Nope'),(question[4], 'Nope'),(question[5], 'Nope')))
            else:
                msg = await bot.send_message(user[0], question[1], reply_markup=inlinekeyboard((question[2], 'Right'),(question[3], 'Nope'),(question[4], 'Nope'),(question[5], 'Nope')))
            msg_id[user[0]]=msg.message_id
    except:
        pass

async def Right_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    print(user_id)
    scoreplus = db.get_inf('Users', 'telegram_id', user_id)[0][3] + score
    await db.update_score(user_id, scoreplus)
    await callback.message.answer(f'Молодец! Это правильный ответ, ты получаешь {score} баллов.')
    await bot.edit_message_reply_markup(user_id, callback.message.message_id, reply_markup=None)
    await callback.answer()

async def Wrong_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.answer('Это неправильный ответ.')
    await bot.edit_message_reply_markup(user_id, callback.message.message_id, reply_markup=None)
    await callback.answer()

async def start(message: types.Message):
    user = db.get_inf('Users', 'telegram_id', message.from_user.id)
    if user:
        reply = f'Привет {message.from_user.first_name}'
        if user[0][-1] == 'user':
            kb = kbc.kb
        elif user[0][-1] == 'admin':
            kb = kbca.kb
    else:
        reply = 'Привет! Это чат бот для квестов! Пожалуйста зарегистрируйся командой /register, если ты не зарегистрировался.'
        kb = kbr.kb
    await message.answer(reply, reply_markup=kb)

async def register(message: types.Message, state:FSMContext):
    RegisterFSM.telegram_id.set()
    async with state.proxy() as data:
        data['telegram_id'] = message.from_user.id
    await RegisterFSM.Name.set() 
    await message.answer('Введи имя', reply_markup=ReplyKeyboardRemove())

async def reg_name(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['Name'] = message.text
    await RegisterFSM.next()
    await message.answer('Введи фамилию')

async def reg_surname(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['Surname'] = message.text
    await RegisterFSM.next()
    await message.answer('Введи почту')

async def reg_email(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['Email'] = message.text
    await db.add_User(state)
    await state.finish()
    await message.answer('Спасибо!', reply_markup=kbc.kb)

async def my_score(message: types.Message):
    user = db.get_inf('Users', 'telegram_id', message.from_user.id)[0]
    await message.answer(f'{message.from_user.first_name} твой счёт {user[3]}.\nСтремись к лучшему!')
    

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(my_score, commands=['my_score'])
    dp.register_message_handler(register, commands=['register'] ,state=None)
    dp.register_message_handler(reg_name, state=RegisterFSM.Name)
    dp.register_message_handler(reg_surname, state=RegisterFSM.Surname)
    dp.register_message_handler(reg_email, state=RegisterFSM.Email)
    dp.register_callback_query_handler(Right_callback,text = 'Right')
    dp.register_callback_query_handler(Wrong_callback,text = 'Nope')