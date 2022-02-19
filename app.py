import os
import logging
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine
from aiogram.bot.api import TelegramAPIServer
from sqlalchemy.orm import scoped_session, sessionmaker

from db import Base
from config import TOKEN, DB_FILENAME, su_admin
#from lang_mid import setup_midlleware


local_server = TelegramAPIServer.from_base('http://localhost')
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)
 
engine = create_engine(f'sqlite:///{DB_FILENAME}')

if not os.path.isfile(f'./{DB_FILENAME}'):
    Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()


#i18n = setup_midlleware(dp)
#_ = i18n.gettext

async def on_shutdown(dp):
    await bot.send_message(su_admin, 'Бот был выключен')


async def on_startup(dp):
    await bot.send_message(su_admin, 'Бот запущен')

if __name__ == '__main__':
    from admin_handlers import dp
    from admin import dp
    from user import dp

    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
    session.close()