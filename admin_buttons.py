from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
import mainbot
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import sqlite3

admin_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Перезапустить бота', callback_data='restart')],
    [InlineKeyboardButton(text='Все равно обратиться', callback_data='support2')],
    [InlineKeyboardButton(text='Просмотреть записи в поддержке', callback_data='view')]
])

admin_reback_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться назад', callback_data='back_admin')]
])

# admib_edit_ctg2_btn = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Изменить документ', callback_data='edit')]
# ])


# Взять на доработку! №
##############################################################################
admin_start_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text= 'Калькулятор', callback_data= 'ctg1')],
    [InlineKeyboardButton(text= 'Конвертор', callback_data= 'ctg2')],
    [InlineKeyboardButton(text='Изменить документацию', callback_data='edit')],
    [InlineKeyboardButton(text='Вернуться назад', callback_data='back')]
])

# admin_edit_button = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Пересоздать кнопки и изменить текст', callback_data=f'reincarnation_')],
#     [InlineKeyboardButton(text='Заменить файлы в существующих кнопках', callback_data='file')]
# ])
# ctg2_btn = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Машинный', callback_data='mech')],
#     [InlineKeyboardButton(text='ИИ', callback_data='ai')],
#     [InlineKeyboardButton(text= 'Вернуться к выбору', callback_data= 'back')]
# ]
##############################################################################


# admin_work_btn = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Отработан', callback_data=f'accept:{i[5]}')]
#     ])

# admin_delete_btn = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Удалить запись', callback_data='del')]
#      ])

async def admin_btns():
    db = sqlite3.connect('support_base_m2.db')
    cur = db.cursor()


    cur.execute('''SELECT hash_file_id, file_name from files''')
    res_all = cur.fetchall()
    print('''КнОпАчКи''', res_all)

    async def markup():
        keyboard = InlineKeyboardBuilder()
        for fi, fn in res_all:
            keyboard.add(InlineKeyboardButton(text=fn, callback_data=f'files_dwn_{fi}'))
        keyboard.add(InlineKeyboardButton(text='Изменить документацию', callback_data=f'edit'),
                     InlineKeyboardButton(text='Вернуться назад', callback_data='back'))
        return keyboard.adjust(1).as_markup()
    return await markup()