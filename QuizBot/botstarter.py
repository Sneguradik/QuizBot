from aiogram import executor
from create import dp
from handlers import client, admin
from database import sqlite_db
import asyncio
import datetime

delay = 20
timestart = 1300
timeend = 2359

async def on_startup(_):
    print('Bot online')
    sqlite_db.on_start()

def checktime():
    now=int(datetime.datetime.now().hour*100 + datetime.datetime.now().minute)
    return (now>=timestart) and (now<=timeend)

def repeat(coro, loop):
    if checktime():
        asyncio.ensure_future(coro(), loop=loop)
        loop.call_later(delay, repeat, coro, loop)



client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(delay, repeat, client.task, loop)
    executor.start_polling( dp, skip_updates=True, on_startup=on_startup, loop=loop )