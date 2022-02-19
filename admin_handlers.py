from aiogram import types
from aiogram.types import message
from aiogram.types.message import ContentType


from app import dp, bot, session
from config import group_id
from db import Admin_g

@dp.message_handler(chat_id=group_id, commands=['locale'])
async def user_checker(message: types.Message):
    await message.answer(message)


@dp.message_handler(chat_id=group_id, content_types=["new_chat_members"])
async def new_chat(message: types.Message):
    x = message.new_chat_members
    for i in x:
        item = Admin_g(user_id=i.id, user_name=i.first_name)
        session.add(item)
        session.commit()
        await message.reply(f'User {i.first_name} - {i.id} was promoted')
   





@dp.message_handler(chat_id=group_id, content_types=["left_chat_member"])
async def left_chat(message: types.Message):
    await message.reply(message.left_chat_member.id)