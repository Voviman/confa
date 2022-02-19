from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, message
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageTextIsEmpty, MessageCantBeEdited, BadRequest
from sqlalchemy import and_
from aiogram.types.message import ContentTypes, ContentType
from aiogram.dispatcher import filters


from app import dp, bot, session
from config import Admin_fsm, re_group_id
from keyboard import admin_kb, admin_res, admin_ques
from db import Base, MediaIds, User, Admin, Admin_g
from localization import local


admins = [487656986, 177837392]

x = session.query(Admin_g).all()
for i in x:
    admins.append(i.user_id)


@dp.message_handler(user_id=admins, commands=['get_admin'], commands_prefix='!')
async def get_admin(message: types.Message):
    for i in admins:
        await message.answer(i)


@dp.message_handler(user_id=admins, commands=['start'])
async def start_ad(message: types.Message):
    await message.answer(f'Ассалому алайкум, {message.from_user.first_name}')


@dp.message_handler(user_id=admins, commands=['type'])
async def types(message: types.Message):
    await message.answer(message)


@dp.message_handler(Text(equals="Посмотреть мои запросы"), user_id=admins)
async def user_req(message):
    x = session.query(Admin).filter_by(admin_id=message.chat.id).order_by(Admin.id.desc()).first()
    if x == None:
        await message.answer('Сизда ҳали ҳеч қандай савол йўқ.')
        return

    text = 'Савол:\n' + f'{x.user_name}\n{x.user_id} \n\n{x.user_text}'
    if x.msg_type == 'text':
        await message.answer(text, reply_markup=admin_res)
    if x.msg_type == 'voice':
        await bot.send_voice(message.chat.id, x.user_text, caption=text, reply_markup=admin_res)


@dp.callback_query_handler(lambda c: c.data == 'ready_ad', state='*')
async def ready_ad(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, call.inline_message_id)
    x = session.query(Admin).filter_by(admin_id=call.message.chat.id).order_by(Admin.id.desc()).first()
    y = session.query(MediaIds).filter_by(user_id=x.user_id).order_by(MediaIds.id.desc()).first()
    lang = session.query(User).filter_by(user_id=x.user_id).first()
    if lang.language == 'ru':
        msg = f'Имомдан жавоб:\n<i>{x.user_text}</i>\n\n<b>{call.message.text}</b>'
        g_msg = f'Савол №: {y.id}\n<code>{x.user_name}</code> \n<b>{x.user_text}</b>\n\n'
        g_msg += f'Саволга берилган жавоб:\n <code>{call.from_user.first_name}</code> \n\n<b>{call.message.text}</b>'
        if x.msg_type == 'text':
            if call.message.text:
                await bot.send_message(x.user_id, msg, parse_mode='html')
                await bot.send_message(re_group_id, g_msg, parse_mode='html')
            if call.message.voice:
                msg = f'Имомдан жавоб:\n<i>{x.user_text}</i>\n\n'
                g_msg = f'Жавоб эгаси: <code>{call.from_user.first_name}</code>\n'
                g_msg += '---------------------------\n'
                g_msg += f'Савол №: {y.id}\n<code>{x.user_name}</code> \n<b>{x.user_text}</b>\n\n'
                await bot.send_voice(x.user_id, call.message.voice.file_id, caption=msg, parse_mode='html')
                await bot.send_voice(re_group_id, call.message.voice.file_id, caption=g_msg, parse_mode='html')
        if x.msg_type == 'voice':
            if call.message.text:
                text = f'Имомдан жавоб:\n<b>{call.message.text}</b>'
                g_text = f'№: {y.id}\nСавол:\n <code>{x.user_name} - {x.user_id}</code> \n\n'
                g_text += f'Саволга берилган жавоб:\n <code>{call.from_user.first_name} - {call.from_user.id}</code>\n\n<b>{call.message.text}</b>'
                await bot.send_voice(x.user_id, x.user_text, caption=text, parse_mode='html')
                await bot.send_voice(re_group_id, x.user_text, caption=g_text, parse_mode='html')
            if call.message.voice:
                msg_q = 'Савол:'
                msg = f' Имомдан жавоб:'
                await bot.send_voice(x.user_id, x.user_text, caption=msg_q, parse_mode='MarkdownV2')
                await bot.send_voice(x.user_id, call.message.voice.file_id, caption=msg, parse_mode='MarkdownV2')

                g_msg = f'№: {y.id}\nСавол:\n`{x.user_name} - {x.user_id}`'
                g_msg_a = f'№: {y.id}\nСаволга берилган жавоб:\n`{call.from_user.first_name} - {call.from_user.id}`'
                await bot.send_voice(re_group_id, x.user_text, caption=g_msg, parse_mode='MarkdownV2')
                await bot.send_voice(re_group_id, call.message.voice.file_id, caption=g_msg_a, parse_mode='MarkdownV2')
    if lang.language == 'en':
        msg = f'Imomdan javob:\n<i>{x.user_text}</i>\n\n<b>{call.message.text}</b>'
        g_msg = f'Савол №: {y.id}\n<code>{x.user_name}</code>\n<b>{x.user_text}</b>\n\n'
        g_msg += f'Саволга берилган жавоб:\n<code>{call.from_user.first_name}</code>\n\n<b>{call.message.text}</b>'
        if x.msg_type == 'text':
            if call.message.text:
                await bot.send_message(x.user_id, msg, parse_mode='html')
                await bot.send_message(re_group_id, g_msg, parse_mode='html')
            if call.message.voice:
                msg = f'Imomdan javob:\n<i>{x.user_text}</i>\n\n'
                g_msg = f'Жавоб эгаси: <code>{call.from_user.first_name}</code> \n'
                g_msg += '---------------------------\n'
                g_msg += f'Савол №: {y.id}\n<code>{x.user_name}</code> \n<b>{x.user_text}</b>\n\n'
                await bot.send_voice(x.user_id, call.message.voice.file_id, caption=msg, parse_mode='html')
                await bot.send_voice(re_group_id, call.message.voice.file_id, caption=g_msg, parse_mode='html')
        if x.msg_type == 'voice':
            if call.message.text:
                msg = f'Imomdan javob:\n<b>{call.message.text}</b>'
                g_msg = f'№: {y.id}\nСавол:\n <code>{x.user_name} - {x.user_id}</code>\n'
                g_msg += f'Саволга берилган жавоб:\n <code>{call.from_user.first_name} - {call.from_user.id}</code> \n\n<b>{call.message.text}</b>'
                await bot.send_voice(x.user_id, x.user_text, caption=msg, parse_mode='html')
                await bot.send_voice(re_group_id, x.user_text, caption=g_msg, parse_mode='html')
            if call.message.voice:
                msg_q = 'Savol:'
                msg = f'Imomdan javob:'
                await bot.send_voice(x.user_id, x.user_text, caption=msg_q, parse_mode='MarkdownV2')
                await bot.send_voice(x.user_id, call.message.voice.file_id, caption=msg, parse_mode='MarkdownV2')

                g_msg = f'№: {y.id}\nСавол:\n`{x.user_name} - {x.user_id}`'
                g_msg_a = f'№: {y.id}\nСаволга берилган жавоб:\n`{call.from_user.first_name} - {call.from_user.id}`'
                await bot.send_voice(re_group_id, x.user_text, caption=g_msg, parse_mode='MarkdownV2')
                await bot.send_voice(re_group_id, call.message.voice.file_id, caption=g_msg_a, parse_mode='MarkdownV2')
    await call.message.answer('Жавобингиз савол эгасига йўлланди')
    session.delete(x)
    session.commit()
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'answer', user_id=admins)
async def answer(call: CallbackQuery):
    await data_saver(call)
    user_info = call.from_user.first_name
    cap = call.message.caption
    if call.message.text:
        y = call.message.text
        z = y.split('\n', 7)
        await call.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{call.message.text}\n\n---------\n<b>Савол қабул қилган Имом - {user_info}</b>', parse_mode='html')
        lang = session.query(User).filter_by(user_id=z[-1]).first()
        if lang.language == 'ru':
            await bot.send_message(z[-1], local.question_proces_k)
        if lang.language == 'en':
            await bot.send_message(z[-1], local.question_proces_l)
        await bot.send_message(call.from_user.id, call.message.text, reply_markup=admin_res)
    if call.message.voice:
        y = call.message.caption
        z = y.split('\n', 3)
        lang = session.query(User).filter_by(user_id=z[-1]).first()
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=f'{call.message.caption}\nСавол қабул қилган Имом - {user_info}')
        await bot.send_voice(call.from_user.id, call.message.voice.file_id, caption=call.message.caption, reply_markup=admin_res)
        if lang.language == 'ru':
            await bot.send_message(z[-1], local.question_proces_k)
        if lang.language == 'en':
            await bot.send_message(z[-1], local.question_proces_l)
    return


@dp.callback_query_handler(lambda c: c.data == 'cancel_ad', state='*')
async def cancel_ad(call: CallbackQuery, state: FSMContext):
    if call.message.text:
        await call.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='бекор қилинди')
        await state.finish()
    if call.message.voice:
        await call.message.delete()
        await call.message.answer('бекор қилинди')
        await state.finish()
    x = session.query(Admin).filter_by(admin_id=call.message.chat.id).order_by(Admin.id.desc()).first()
    msg = f'Савол:{x.user_name}\n{x.user_id}\n\n{x.user_text}'
    if x.msg_type == 'text':
        await call.message.answer(msg, reply_markup=admin_res)
    if x.msg_type == 'voice':
        await call.message.answer_voice(x.user_text, caption=msg, reply_markup=admin_res)


@dp.callback_query_handler(lambda c: c.data == 'admin_answer')
async def admin_answer(call: CallbackQuery):
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, call.inline_message_id)
    if call.message.text:
        await call.message.answer(f'Жавобингизни йўлланг')
    if call.message.voice:
        await call.message.answer(f'Жавобингизни йўлланг')

    await Admin_fsm.check.set()


@dp.message_handler(user_id=admins, state=Admin_fsm.check, content_types=[ContentType.VOICE, ContentType.TEXT])
@dp.message_handler(content_types='voice')
@dp.message_handler(content_types=ContentTypes.VOICE)
async def msg_confirm(message):
    if message.text:
        await message.answer(message.text, reply_markup=admin_ques)
    elif message.voice:
        await message.answer_voice(message.voice.file_id, reply_markup=admin_ques)
    else:
        await message.answer('Саволингиз аудио ёки техт форматда болиши керак!')


async def data_saver(call):
    if call.message.text:
        y = call.message.text
        z = y.split('\n', 4)
        newItem = Admin(admin_id=call.from_user.id, user_id=z[-1], user_name=z[1], user_text=z[3], msg_type='text')
        session.add(newItem)
        session.commit()
    if call.message.voice:
        cap = call.message.caption
        x = cap.split('\n', 3)
        newItem = Admin(admin_id=call.from_user.id, user_id=x[-1], user_name=x[1], user_text=call.message.voice.file_id, msg_type='voice')
        session.add(newItem)
        session.commit()

    '''
    if call.message.video_note:
        y = f"'{call.message.video_note.file_id}'"
        await call.message.answer(y)
        x = session.query(MediaIds).filter_by(user_text=y).first()
        await call.message.answer(x.user_text)
        newItem = Admin(admin_id=call.from_user.id, user_id=x.user_id, user_name=x.user_name, user_text=x.user_text, msg_type=x.msg_type)
        session.add(newItem)
        session.commit()
    '''

async def edited_msg(call, text):
    try:
        await call.bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text)
    except (MessageCantBeEdited, MessageTextIsEmpty, BadRequest):
        await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=text)
    except Exception as e:
        await call.message.answer(e)
        return