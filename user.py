from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types.message import ContentTypes
from aiogram.utils.exceptions import MessageTextIsEmpty, MessageCantBeEdited, BadRequest
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove


from app import dp, bot, session
from db import MediaIds, User, Admin
from config import group_id, admins, Form, text
from keyboard import response_kb, ques, res, lang, response_kb_l
from localization import local



async def get_lang(message):
    x = session.query(User).filter_by(user_id=message.chat.id).first()
    if x.language == None:
        msg = f'{local.lang_set_k}/{local.lang_set_l}'
        await message.answer(msg, reply_markup=lang)

    if x.language == 'ru':
        await message.answer(local.lang_set_k, reply_markup=lang)

    if x.language == 'en':
        await message.answer(local.lang_set_l, reply_markup=lang)


@dp.message_handler(commands=['start'], state='*')
async def start_msg(message: types.Message):
    x = session.query(User).filter_by(user_id=message.chat.id).first()
    msg = f'{local.start_msg}{message.from_user.mention}'
    lang = session.query(User).filter_by(user_id=message.chat.id).first()
    if x == None:
        await message.reply(msg, reply_markup=response_kb)
        newItem = User(user_id=message.chat.id)
        print(x)
        session.add(newItem)
        session.commit()
        await get_lang(message)
        await Form.manager.set()

    else:
        if lang.language == 'ru':
            await message.reply(msg, reply_markup=response_kb)

        if lang.language == 'en':
            msg = f'{local.start_msg_l}{message.from_user.mention}'
            await message.reply(msg, reply_markup=response_kb_l)
        await Form.manager.set()

@dp.callback_query_handler(lambda c: c.data == 'eng', state='*')
async def switch_eng(call: CallbackQuery):
    lang = session.query(User).filter_by(user_id=call.message.chat.id).first()
    lang.language = 'en'
    session.commit()
    text = local.lang_switch_l
    await call.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text)
    await start_msg(call.message)


@dp.callback_query_handler(lambda c: c.data == 'rus', state='*')
async def switch_rus(call: CallbackQuery):
    lang = session.query(User).filter_by(user_id=call.message.chat.id).first()
    lang.language = 'ru'
    session.commit()
    text = local.lang_switch_k
    await call.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text)
    await start_msg(call.message)



@dp.message_handler(commands=['get_user'])
async def get_users(message: types.Message):
    users = await bot.get_chat_members_count(message.chat.id)
    chat = bot.get_current(message.chat.id)
    argument = message.get_args()
    await message.answer(argument)
    for i in chat:
        await message.answer(i)


@dp.message_handler(commands=['get_all'])
async def get_all(message: types.Message):
    ourUser = session.query(MediaIds).all()
    for i in ourUser:
        text = (i.user_id, i.user_text)
        await bot.send_message(message.chat.id, text)


@dp.message_handler(commands=['id'])
async def grab_id(message: types.Message):
    await message.reply(message.chat.id)


@dp.message_handler()
async def msg_listener(message: types.Message, state: FSMContext):
    await manager(message, state)



@dp.message_handler(Text(equals="САВОЛ БЕРИШ УЧУН БОСИНГ ✉️"), content_types=[ContentTypes.TEXT, ContentTypes.VOICE, ContentTypes.VIDEO_NOTE])
@dp.message_handler(state=Form.manager)
async def manager(message: types.Message, state: FSMContext):
    lang = session.query(User).filter_by(user_id=message.chat.id).first()

    if message.text == 'САВОЛ БЕРИШ УЧУН БОСИНГ ✉️' or message.text == 'SAVOL BERISH UCHUN BOSING ✉️':
        if lang.language == 'ru':
            await message.answer(local.taking_response_k, reply_markup=ReplyKeyboardRemove())
        if lang.language == 'en':
            await message.answer(local.taking_response_l, reply_markup=ReplyKeyboardRemove())
        await Form.analz.set()

    elif message.text == '⚙️':
        await get_lang(message)

    else:
        if lang.language == 'ru':
                await message.answer(local.incorrect_in_k)
                return

        if lang.language == 'en':
            await message.answer(local.incorrect_in_l)
            return
   

@dp.message_handler(state=Form.analz, content_types=ContentTypes.ANY)
async def analz_type(message: types.Message):
    lang = session.query(User).filter_by(user_id=message.chat.id).first()
    if message.text:
        await message.answer(message.text, reply_markup=ques)
    
    elif message.voice:
        await bot.send_voice(message.chat.id, message.voice.file_id, reply_markup=ques)

    else: 
        if lang.language == 'ru':
            await message.answer(local.error_input_k, reply_markup=response_kb)
        if lang.language == 'en':
            await message.answer(local.error_input_l, reply_markup=response_kb_l)


@dp.callback_query_handler(state='*')
async def done(call: CallbackQuery):
    lang = session.query(User).filter_by(user_id=call.message.chat.id).first()
    if call.data == 'ready':
        await sender(call)
        await Form.manager.set()
        try:
            if lang.language == 'ru':
                await call.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=local.question_added_k, reply_markup=response_kb)
            if lang.language == 'en':
                await call.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=local.question_added_l, reply_markup=response_kb_l)
        except (MessageCantBeEdited, MessageTextIsEmpty, BadRequest):
            await call.bot.delete_message(call.message.chat.id, call.message.message_id)
            if lang.language == 'ru':
                await call.message.answer(local.question_added_k, reply_markup=response_kb)
            
            if lang.language == 'en':
                await call.message.answer(local.question_added_l, reply_markup=response_kb_l)
        except Exception as e:
            await call.message.answer(e)
            return
    if call.data == 'cancel':
        await Form.manager.set()
        try:
            if lang.language == 'ru':
                await call.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=local.question_canceled_k, reply_markup=response_kb)

            if lang.language == 'en':
                await call.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=local.question_canceled_l, reply_markup=response_kb_l)
        except (MessageCantBeEdited, MessageTextIsEmpty, BadRequest):
            await call.bot.delete_message(call.message.chat.id, call.message.message_id)
            if lang.language == 'ru':
                await call.message.answer(local.question_canceled_k, reply_markup=response_kb)

            if lang.language == 'en':
                await call.message.answer(local.question_canceled_l, reply_markup=response_kb_l)

        except Exception as e:
            await call.message.answer(e)
            return


async def sender(x):
    chat = await bot.get_chat(x.message.chat.id)
    msg = f'<b>Савол:</b>\n{chat.first_name}(@{chat.username})'
    await Form.manager.set()
    if x.message.video_note:
        await bot.send_video_note(group_id, x.message.video_note.file_id, reply_markup=res)
        newItem = MediaIds(user_id=chat.id, user_name=str(chat.first_name), user_text=x.message.video_note.file_id, msg_type='video_note')
        session.add(newItem)
        session.commit()

    elif x.message.voice:
        await bot.send_voice(group_id, x.message.voice.file_id, caption=f'{msg}\n<i>{chat.id}</i>', reply_markup=res, parse_mode='html')
        newItem = MediaIds(user_id=chat.id, user_name=str(chat.first_name), user_text=x.message.voice.file_id, msg_type='voice')
        session.add(newItem)
        session.commit()

    elif x.message.text:
        await bot.send_message(group_id, f'{msg}\n\n "<b>{x.message.text}</b>"\n\n<i>{chat.id}</i>', parse_mode='html', reply_markup=res)
        newItem = MediaIds(user_id=chat.id, user_name=str(chat.first_name), user_text=str(x.message.text), msg_type='text')
        session.add(newItem)
        session.commit()

    else:
        await error(x)


async def error(x):
    await Form.manager.set()
    await x.answer('Ошибка')