import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, URLInputFile, BufferedInputFile, CallbackQuery, ContentType, InputFile
import logging
import os
import tempfile
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import sqlite3
import subprocess
import time
import hashlib
from io import BytesIO

from cnf import TOKEN
import buttons_bot as bb
import admin_buttons as ab

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class supports_tm(StatesGroup):
    supp_txt = State()
    number = State()
    adm_edit = State()
    wait_f = State()

async def main():
    await dp.start_polling(bot)

@dp.message(CommandStart())
async def start_msg(message: Message):
    if message.from_user.id == 745764314:
        await message.answer('''Добро пожаловать!✋
Это бот для навигации сотрудников по работе с задачами нашей компании.
Выберите один из пунктов для продолжения работы💻: ''', reply_markup= await ab.admin_btns())
    else:
        await message.answer('''Добро пожаловать!✋
Это бот для навигации сотрудников по работе с задачами нашей компании.
Выберите один из пунктов для продолжения работы💻: ''', reply_markup= await bb.btns())

@dp.message(Command('support'))
async def supp(message: Message):
    a = message.from_user.id
    if a == 745764314:
        await message.answer('''❓Если у вас возникли проблемы при работе с CRM, то обратитесь в поддержку''', reply_markup=ab.admin_btn)
    else:
        print(message.from_user.id)
        await message.answer('''❓Если у вас возникли проблемы при работе с CRM, то обратитесь в поддержку''', reply_markup=bb.support_btn2)

@dp.callback_query(F.data == 'back_admin')
async def supp(callback: CallbackQuery):
    a = callback.from_user.id
    if a == 745764314:
        await callback.message.edit_text('''❓Если у вас возникли проблемы при работе с CRM, то обратитесь в поддержку''', reply_markup=ab.admin_btn)
    else:
        print(callback.from_user.id)
        await callback.message.edit_text('''❓Если у вас возникли проблемы при работе с CRM, то обратитесь в поддержку''', reply_markup=bb.support_btn2)

@dp.callback_query(F.data == 'view')
async def view_supp(callback: CallbackQuery):
    db = sqlite3.connect('support_base_m2.db')
    cur = db.cursor()
    cur.execute('''SELECT id, idnp, tgname, number, text_supp, queue, status from supports''')
    admin_res = cur.fetchall()
    print(admin_res)
    if admin_res == []:
        await callback.message.edit_text('''❗️Пока нет ни одного обращения  в поддержку''', reply_markup=ab.admin_reback_btn)
    else:
        for i in admin_res:
            if i[6] == 'решается🛠':
                admin_work_btn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Отработан', callback_data=f'accept:{i[0]}')]
            ])
                await callback.message.answer(f'''id: {i[1]}
🔤 Никнейм: <u>{i[2]}</u>
📞 Номер телефона: {i[3]}
📩 Обращение: {i[4]}
🗂 Очередь: {i[5]}
🕐 Статус: {i[6]} ''', reply_markup=admin_work_btn, parse_mode="HTML")
            else:
                admin_worked_btn = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Удалить запись', callback_data=f'del:{i[0]}')]
                ])
                await callback.message.answer(f'''id: {i[1]}
🔤 Никнейм: <u>{i[2]}</u>
📞 Номер телефона: {i[3]}
📩 Обращение: {i[4]}
🗂 Очередь: {i[5]}
🕐 Статус: {i[6]} ''', reply_markup=admin_worked_btn, parse_mode="HTML")
        
@dp.callback_query(F.data.startswith('accept:'))
async def process_callback_change_record(callback: CallbackQuery):
    record_id = str(callback.data.split(':')[1])
    print(record_id)
    admin_delete_btn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Удалить запись', callback_data=f'del:{record_id}')]
     ])
    await acc_supp(record_id)
    await bot.answer_callback_query(callback.id)
    await callback.message.edit_text("📝 Запись успешно изменена!", reply_markup=admin_delete_btn)

async def acc_supp(record_id):
    db = sqlite3.connect('support_base_m2.db')
    cur = db.cursor()
    cur.execute(f'''SELECT queue from supports WHERE id == {record_id}''')
    queue_rec = cur.fetchone()
    nb = ' '.join(map(str, queue_rec))
    nnb = int(nb) - 1
    print(nnb)
    cur.execute('''UPDATE supports SET status = ? WHERE  id = ?''', ('Отработано ✅', record_id))
    cur.execute('''UPDATE supports SET queue = queue - 1''')
    db.commit()
    db.close()

@dp.callback_query(F.data.startswith('del:'))
async def delete_rec(callback: CallbackQuery):
    record_id2 = str(callback.data.split(':')[1])
    print(record_id2)
    await delete_r(record_id2)
    await bot.answer_callback_query(callback.id)
    await callback.message.edit_text("🗑 Запись успешно удалена!", reply_markup=ab.admin_reback_btn)

async def delete_r(record_id2):
    db = sqlite3.connect('support_base_m2.db')
    cur = db.cursor()
    cur.execute('''DELETE from supports WHERE id = ?''', (record_id2))
    cur.execute('''UPDATE supports SET queue = queue - 1 WHERE status = 'решается🛠' ''')
    db.commit()
    db.close()

@dp.callback_query(F.data == 'support2')
async def supp(callback: CallbackQuery):
    await callback.message.edit_text('''👨‍🔧 Вы обращаетесь в поддержку
Напишите ваши претензии и мы поможем вам! 
Все обращения записываются в порядке очереди, будьте терпеливы при ожидании обратной связи. 
С вами обязательно свяжутся!
Чтобы мы смогли вам помочь лучше, напишите ваше обращение в таком формате:

🔹 Не отправляется документ 'название документа' 
🔹 Не работает оформление заказа''', reply_markup= bb.support_btn)

@dp.callback_query(F.data == 'restart')
async def res_bt(callback: CallbackQuery):
    subprocess.Popen(['python3', '/Users/evgeniya/Desktop/PYTHON/botGPS/mainbot.py'])
    await bot.answer_callback_query(callback.id)
    await callback.message.edit_text("Перезапуск 3️⃣...")
    time.sleep(1)
    await callback.message.edit_text("Перезапуск 2️⃣...")
    time.sleep(1)
    await callback.message.edit_text("Перезапуск 1️⃣...")
    time.sleep(1)
    await callback.message.edit_text("🤖 Бот успешно перезапущен!", reply_markup=bb.backkk_btn)

@dp.callback_query(F.data == 'go')
async def supp_enter(callback: CallbackQuery, state: FSMContext):
    await state.set_state(supports_tm.supp_txt)
    await callback.message.edit_text(f'{callback.from_user.full_name}, Введите ваше обращение:')

@dp.message(supports_tm.supp_txt)
async def reg_supp(message: Message, state: FSMContext):
    await state.update_data(supp_txt=message.text)
    await state.set_state(supports_tm.number)
    await message.answer('''Отправьте ваш номер телефона''')

@dp.message(supports_tm.number)
async def reg_numb(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    db = sqlite3.connect('support_base_m2.db')
    cur = db.cursor()
    txt = await state.get_data()
    print(txt)
    cur.execute('''SELECT queue from supports ORDER BY ROWID DESC LIMIT 1''')
    queue = cur.fetchone()
    print(queue)
    if queue == None:
        que = '1'
    else:
        convert = " ".join(map(str, queue))
        que = int(convert) + 1
    cur.execute('''INSERT INTO supports (idnp, tgname, number, text_supp, queue) VALUES (?, ?, ?, ?, ?)''', [message.from_user.id,f'@{message.from_user.username}', txt['number'], txt['supp_txt'], que])
    cur.execute('''SELECT queue from supports ORDER BY ROWID DESC LIMIT 1''')
    res = cur.fetchone()
    await message.reply(f'''📄 Ваше обращение записано! Ожидайте обратной связи. 
🗂 Очередь: {' '.join(map(str, res))}''', reply_markup=bb.status_btn)
    state.clear()
    db.commit()
    db.close()

@dp.callback_query(F.data == 'status')
async def status(callback: CallbackQuery):
    db = sqlite3.connect('support_base_m2.db')
    cur = db.cursor()
    cur.execute(f'''SELECT tgname from supports WHERE idnp == {callback.from_user.id} ORDER BY ROWID DESC LIMIT 1''')
    name = cur.fetchone()
    cur.execute(f'''SELECT number from supports WHERE idnp == {callback.from_user.id} ORDER BY ROWID DESC LIMIT 1''')
    numb = cur.fetchone()
    cur.execute(f'''SELECT text_supp from supports WHERE idnp == {callback.from_user.id} ORDER BY ROWID DESC LIMIT 1''')
    txt_tg = cur.fetchone()
    cur.execute(f'''SELECT queue from supports WHERE idnp == {callback.from_user.id} ORDER BY ROWID DESC LIMIT 1''')
    qq = cur.fetchone()
    cur.execute(f'''SELECT status from supports WHERE idnp == {callback.from_user.id} ORDER BY ROWID DESC LIMIT 1''')
    st = cur.fetchone()
    if name == None:
        await callback.message.edit_text('''❗️Вы еще ни разу не писали в поддержку!
Либо ваша запись была отработана и удалена''', reply_markup=bb.reback_btn)
    else:
        await callback.message.edit_text(f'''🔠 Никнейм: {name[0]} 
📞 Номер: {numb[0]}
📨 Обращение: {txt_tg[0]}
🗂 Очередь: {qq[0]}
🕐 Статус: {st[0]}''', reply_markup=bb.reback_btn)
    
@dp.callback_query(F.data == 'back')
async def menu_b(callback: CallbackQuery):
    if callback.from_user.id == 745764314:
        await callback.message.answer('''Добро пожаловать!✋
Это бот для навигации сотрудников по работе с задачами нашей компании.
Выберите один из пунктов для продолжения работы💻: ''', reply_markup= await ab.admin_btns())
    else:
        await callback.message.answer('''Добро пожаловать!✋
Это бот для навигации сотрудников по работе с задачами нашей компании.
Выберите один из пунктов для продолжения работы💻: ''', reply_markup= await bb.btns())
        
@dp.callback_query(F.data == 'edit')
async def admin_edit_file(callback: CallbackQuery, state: FSMContext):
    db = sqlite3.connect('support_base_m2.db')
    cur = db.cursor()
    await callback.message.edit_text(f'{callback.from_user.full_name}, для изменения документации, отправьте все файлы, которые вы хотите внести: ', reply_markup=bb.backkk_btn)
    await state.set_state(supports_tm.wait_f)
    cur.execute('''DELETE from files''')
    db.commit()
    db.close()

@dp.callback_query(F.data == 'ctg1')
async def category_1(callback: CallbackQuery):
    await callback.message.reply_document(document=FSInputFile('/Users/evgeniya/Desktop/PYTHON/botGPS/TestDocs/instr_calc.pdf'), caption= '''Документация по использованию калькулятора👨‍💻: ''', reply_markup=bb.backkk_btn)

@dp.message(supports_tm.wait_f)
async def save_files(message: Message, state: FSMContext):
    db = sqlite3.connect('support_base_m2.db')
    cur = db.cursor()
    data = await state.get_data()
    files = data.get('files', [])
    send_save_message = data.get('send_save_message', False)
    if message.document:
        file_id = message.document.file_id
        hash_file = hashlib.md5(file_id.encode()).hexdigest()[:16]
        file_name = message.document.file_name
        print(hash_file, file_name)
        files.append((file_id, hash_file, file_name))
        cur.execute('''INSERT INTO files (file_id, hash_file_id, file_name) VALUES (?, ?, ?)''', (file_id, hash_file, file_name))
    await state.update_data(files=files, send_save_message=True)
    db.commit()
    db.close()

    if not send_save_message:
        admin_save_btn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Да, сохранить', callback_data=f'sf')],
            [InlineKeyboardButton(text='Отмена', callback_data='back')]
        ])
        await message.answer('''Сохранить данные файл(ы)?''', reply_markup=admin_save_btn)

@dp.callback_query(F.data.startswith('sf'))
async def save_file_db(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    files = data.get('files', [])
    print("Гетка", files)

    db = sqlite3.connect('support_base_m2.db')
    cur = db.cursor()
    for file_id, hash_id, file_name in files:
        file = await bot.get_file(file_id)
        f_data = await bot.download_file(file.file_path)
        bytes_f = f_data.getvalue()
        cur.execute(f'''UPDATE files SET file = ? WHERE  hash_file_id = ?''', (sqlite3.Binary(bytes_f), hash_id))

    cur.execute('''SELECT hash_file_id, file_name from files''')
    res_all = cur.fetchall()
    print('''КнОпАчКи''', res_all)

    async def markup():
        keyboard = InlineKeyboardBuilder()
        for fi, fn in res_all:
            keyboard.add(InlineKeyboardButton(text=fn, callback_data=f'files_dwn{fi}'))
        keyboard.add(InlineKeyboardButton(text='Вернуться назад', callback_data='back'))
        return keyboard.adjust(1).as_markup()

    await callback.message.edit_text('''Вы отредактировали документацию!''', reply_markup=await markup())
    await state.clear()
    db.commit()
    db.close()

@dp.callback_query(F.data.startswith('files_dwn_'))
async def ff(callback: CallbackQuery, state: FSMContext):
    db = sqlite3.connect('support_base_m2.db')
    cur = db.cursor()
    file_idd = callback.data.split('_')[2]
    print(file_idd)
    cur.execute('''SELECT file, file_name from files WHERE hash_file_id = ?''', [file_idd])
    res_res = cur.fetchone()

    if res_res:
        d_file, n_file = res_res

        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(n_file)[1]) as temp_file:
            temp_file.write(d_file)
            temp_file_path = temp_file.name
            print('темпушка',temp_file_path)
        await callback.message.reply_document(document=FSInputFile(temp_file_path), caption='Ваша документация: ', reply_markup=bb.backkk_btn)
        os.remove(temp_file_path)
    else:
        await callback.message.answer('''Такого файла не существует!''', reply_markup=bb.backkk_btn)

@dp.callback_query(F.data == 'ctg2')
async def category_1(callback: CallbackQuery):
    if callback.from_user.id == 745764314:
        pass
    else:
        await callback.message.answer('''📚 Выберите документацию:''', reply_markup= bb.ctg2_btn)

@dp.callback_query(F.data == 'mech')
async def d_one(callback: CallbackQuery):
    await callback.message.reply_document(document=FSInputFile('/Users/evgeniya/Desktop/PYTHON/botGPS/TestDocs/mech.docx'), caption= '''Документация по использованию машинного конвертора👨‍💻: ''', reply_markup=bb.backkk_btn)

@dp.callback_query(F.data == 'ai')
async def d_two(callback: CallbackQuery):
    await callback.message.reply_document(document=FSInputFile('/Users/evgeniya/Desktop/PYTHON/botGPS/TestDocs/ai.docx'), caption= '''Документация по использованию ИИ конвертора👨‍💻: ''', reply_markup=bb.backkk_btn)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt or RuntimeError:
        print("Bot was disabled")