from aiogram.dispatcher.filters.state import State, StatesGroup
import os
from pathlib import Path

TOKEN = '1430379761:AAElnzXVmgeUdVDSHBSj9dAZ8oVynGHwmY4'
admins = [487656986, 1850643439, 177837392]
group_id = -706852753
re_group_id = -415458276
end = 'запрос принят'
su_admin = 487656986

DB_FILENAME = 'botuploads.db'
I18N_DOMAIN = 'fdbk'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'


class Form(StatesGroup):
    manager = State()
    analz = State()
    text = State()
    audio = State()
    video = State()

class Send(StatesGroup):
    ques = State()
    ready = State()

class Admin_fsm(StatesGroup):
    send_resp = State()
    check = State()
    cancel = State()

class text():
    start = '''Напишите сообщение 
	Savolingizni yozing 
	Саволингизни йозинг'''
    
    cmpt = '''Запрос принят
    Qabul qilindi
	Кабул килинди'''
    
    audio = '''Запишите аудио сообщение
	Audio xabar yozing
	Аудио хабар йозинг'''
    
    video = '''Запишите видео сообщение
	Video xabar yozing
	Видео хабар йозинг'''