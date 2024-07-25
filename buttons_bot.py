from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

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

support_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Приступить', callback_data='go')],
    [InlineKeyboardButton(text= 'Вернуться к выбору', callback_data='back')]
    ]) 