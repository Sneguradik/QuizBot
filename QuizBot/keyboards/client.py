from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from random import choice
class ComandKeyboard:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    def __init__(self,one_time,*args) -> None:
        self.kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
        for b in args:
            self.kb.add(b)

kbr = ComandKeyboard(False,'/register')  
kbc = ComandKeyboard(True,'/my_score') 
 
class InlineKeyboard:
    kb = InlineKeyboardMarkup(row_width=2)
    def __init__(self, *args):
        self.kb.clean()
        args = list(args)
        for i in range(len(args)):
            elem = choice(args)
            args.remove(elem)
            self.kb.add(InlineKeyboardButton(elem[0], callback_data=elem[1]))
def inlinekeyboard(*args):
    kb = InlineKeyboardMarkup(row_width=2)
    args = list(args)
    for i in range(len(args)):
        elem = choice(args)
        args.remove(elem)
        kb.add(InlineKeyboardButton(elem[0], callback_data=elem[1]))
    return kb