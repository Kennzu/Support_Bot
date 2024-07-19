import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, URLInputFile, BufferedInputFile, CallbackQuery
import logging
import os
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

from cnf import TOKEN
import buttons_bot as bb

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)

@dp.message(CommandStart())
async def start_msg(message: Message):
    await message.answer('''Добро пожаловать!✋
Это бот для навигации сотрудников по работе с задачами нашей компании.
Выберите один из пунктов для продолжения работы💻: ''', reply_markup= bb.start_btn)

@dp.callback_query(F.data == 'back')
async def menu_b(callback: CallbackQuery):
    await callback.message.answer('''Добро пожаловать!✋
Это бот для навигации сотрудников по работе с задачами нашей компании.
Выберите один из пунктов для продолжения работы💻: ''', reply_markup= bb.start_btn)

@dp.callback_query(F.data == 'ctg1')
async def category_1(callback: CallbackQuery):
    await callback.message.answer('''Выберите документацию:''', reply_markup= bb.ctg1_btn)

@dp.callback_query(F.data == 'set')
async def d_one(callback: CallbackQuery):
    await callback.message.reply_document(document=FSInputFile('TestDocs/webcalc.docx'), caption= '''Документация по использованию веб-калькулятора👨‍💻: ''', reply_markup=bb.backkk_btn)

@dp.callback_query(F.data == 'loc')
async def d_one(callback: CallbackQuery):
    await callback.message.reply_document(document=FSInputFile('TestDocs/loccalc.docx'), caption= '''Документация по использованию локального калькулятора👨‍💻: ''', reply_markup=bb.backkk_btn)

@dp.callback_query(F.data == 'ctg2')
async def category_1(callback: CallbackQuery):
    await callback.message.answer('''Выберите документацию:''', reply_markup= bb.ctg2_btn)

@dp.callback_query(F.data == 'mech')
async def d_one(callback: CallbackQuery):
    await callback.message.reply_document(document=FSInputFile('TestDocs/mech.docx'), caption= '''Документация по использованию машинного конвертора👨‍💻: ''', reply_markup=bb.backkk_btn)

@dp.callback_query(F.data == 'ai')
async def d_one(callback: CallbackQuery):
    await callback.message.reply_document(document=FSInputFile('TestDocs/ai.docx'), caption= '''Документация по использованию ИИ конвертора👨‍💻: ''', reply_markup=bb.backkk_btn)

@dp.callback_query(F.data == 'ctg3')
async def category_1(callback: CallbackQuery):
    await callback.message.answer('''Ко всем вопросам в службу поддержки
89999999999 - номер горячей линии
89999999999 - номер оператора
@tgtgtgtgtg - телеграмм службы поддержки
@gtgtgtgtgt - телеграмм оператора бота''',reply_markup=bb.backkk_btn)

# @dp.callback_query(F.data == 'Docs1')
# async def d_one(callback: CallbackQuery):
#     await callback.message.reply_document(document=FSInputFile('TestDocs/Docu1.docx'), caption= '''Документация к первичным задачам компании👨‍💻: ''', reply_markup=bb.backkk_btn)

# @dp.callback_query(F.data == 'Docs2')
# async def d_two(callback: CallbackQuery):
#     await callback.message.reply_document(document=FSInputFile('TestDocs/Docu2.docx'), caption= '''Документация к вторичным задачам компании👩‍💻: ''', reply_markup=bb.backkk_btn)

# @dp.callback_query(F.data == 'Docs3')
# async def d_three(callback: CallbackQuery):
#     await callback.message.reply_document(document=FSInputFile('TestDocs/Docu3.docx'), caption= '''Документация к третичным задачам компании👥: ''', reply_markup=bb.backkk_btn)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt or RuntimeError:
        print("Bot was disabled")