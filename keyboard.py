from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


button_text = KeyboardButton('SAVOL BERISH UCHUN BOSING ✉️')
button_text_l = KeyboardButton('САВОЛ БЕРИШ УЧУН БОСИНГ ✉️')
button_lang = KeyboardButton('⚙️')
button_admin = KeyboardButton('Саволларимни кўриш')

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_kb.add(button_admin)
response_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
response_kb.add(button_text, button_lang)
response_kb_l = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
response_kb_l.add(button_text_l, button_lang)

ques = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data="ready"),
            InlineKeyboardButton(text="❌", callback_data="cancel")
        ]
    ]
)

admin_ques = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data="ready_ad"),
            InlineKeyboardButton(text="❌", callback_data="cancel_ad")
        ]
    ]
)

lang = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Lotin', callback_data='eng'),
            InlineKeyboardButton(text='Ўзбек', callback_data='rus')
        ]
    ]
)

res = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Жавоб бериш', callback_data='answer')
        ]
    ]
)

admin_res = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Жавоб бериш', callback_data='admin_answer')
        ]
    ]
)
