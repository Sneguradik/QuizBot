from aiogram import Dispatcher, types 
from create import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import database.sqlite_db as db 
from keyboards.client import *
from keyboards.admin import *

class QuestionsFSM(StatesGroup):
    Question = State()
    RightAnswer = State()
    Answer1 = State()
    Answer2 = State()
    Answer3 = State()
    Score = State()
    file_id = State()

async def AllQuestions(message: types.Message):
    if db.get_inf('Users', 'telegram_id', message.from_user.id)[0][-1] == 'admin':
        questions = db.get_inf('Questions')
        for question in questions:
            reply = f''' 
            ID:{question[0]}\n
            Вопрос: {question[1]}\n
            Правильный ответ: {question[2]}\n
            Ответ 1: {question[3]}\n
            Ответ 2: {question[4]}\n
            Ответ 3: {question[5]}\n
            Балл за правильный ответ:{question[6]}\n
            '''
            if question[7]!=0:
                await message.answer_photo(question[7], caption=reply)
            else:
                await message.answer(reply)

async def AddQuestion(message: types.Message, state:FSMContext):
    if db.get_inf('Users', 'telegram_id', message.from_user.id)[0][-1] == 'admin':
        await QuestionsFSM.Question.set()
        await message.answer('Введи вопрос', reply_markup=ReplyKeyboardRemove())

async def reg_Question(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['Question'] = message.text
    await QuestionsFSM.next()
    await message.answer('Введи правильный ответ')

async def reg_RightAnswer(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['RightAnswer'] = message.text
    await QuestionsFSM.next()
    await message.answer('Введи первый неправильный ответ')

async def reg_Answer1(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['Answer1'] = message.text
    await QuestionsFSM.next()
    await message.answer('Введи второй неправильный ответ')

async def reg_Answer2(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['Answer2'] = message.text
    await QuestionsFSM.next()
    await message.answer('Введи третий неправильный ответ')

async def reg_Answer3(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['Answer3'] = message.text
    await QuestionsFSM.next()
    await message.answer('Введи количество баллов за правильный ответ')

async def reg_Score(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['Score'] = int(message.text)
    await QuestionsFSM.next()
    await message.answer('Загрузи фотографию, если она есть. Если её нет, то введи 0.')
   

async def reg_photo(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        if message.photo:
            x=message.photo[0].file_id
        else:
            x='0'
        data['file_id'] = x
    await db.add_Question(state)
    await state.finish()
    await message.answer('Спасибо!', reply_markup=kbca.kb)
 
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler( AllQuestions, commands=['AllQuestions'])
    dp.register_message_handler( AddQuestion, commands=['AddQuestion'], state=None)
    dp.register_message_handler(reg_Question , state=QuestionsFSM.Question)
    dp.register_message_handler(reg_RightAnswer , state=QuestionsFSM.RightAnswer)
    dp.register_message_handler(reg_Answer1 , state=QuestionsFSM.Answer1)
    dp.register_message_handler(reg_Answer2, state=QuestionsFSM.Answer2)
    dp.register_message_handler(reg_Answer3 , state=QuestionsFSM.Answer3)
    dp.register_message_handler(reg_Score, state=QuestionsFSM.Score)
    dp.register_message_handler( reg_photo , state=QuestionsFSM.file_id, content_types=['photo','text'] )
