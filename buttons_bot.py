from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sqlite3

# start_btn = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text= 'Документация 1', callback_data= 'Docs1')],
#     [InlineKeyboardButton(text= 'Документация 2', callback_data= 'Docs2')],
#     [InlineKeyboardButton(text= 'Документация 3', callback_data= 'Docs3')]
# ])

start_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text= 'Калькулятор', callback_data= 'ctg1')],
    [InlineKeyboardButton(text= 'Конвертор', callback_data= 'ctg2')],
])

# ctg1_btn = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text= 'Сетевой', callback_data= 'set')],
#     [InlineKeyboardButton(text= 'Локальный', callback_data= 'loc')],
#     [InlineKeyboardButton(text= 'Вернуться к выбору', callback_data= 'back')]
#     ]
# )


ctg2_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Машинный', callback_data='mech')],
    [InlineKeyboardButton(text='ИИ', callback_data='ai')],
    [InlineKeyboardButton(text= 'Вернуться к выбору', callback_data= 'back')]
])

backkk_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text= 'Вернуться к выбору', callback_data= 'back')]
])

reback_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text= 'Вернуться назад', callback_data= 'support2')]
])

support_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Приступить', callback_data='go')], [InlineKeyboardButton(text='Посмотреть статуст запроса', callback_data='status')],
    [InlineKeyboardButton(text= 'Вернуться к выбору', callback_data='back')],
    ]) 

support_btn2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обратиться в поддержку', callback_data='support2')]
])
status_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Посмотреть статус запроса', callback_data='status')],
    [InlineKeyboardButton(text='Вернутсья к выбору', callback_data='back')]
])

# restart_btn = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Перезапустить бота')]
#     ])

async def btns():
    db = sqlite3.connect('support_base_m2.db')
    cur = db.cursor()


    cur.execute('''SELECT hash_file_id, file_name from files''')
    res_all = cur.fetchall()
    print('''КнОпАчКи''', res_all)

    async def markup():
        keyboard = InlineKeyboardBuilder()
        for fi, fn in res_all:
            keyboard.add(InlineKeyboardButton(text=fn, callback_data=f'files_dwn_{fi}'))
        return keyboard.adjust(1).as_markup()
    return await markup()
