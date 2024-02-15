#Импорт библиотек
import asyncio, re, datetime
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram import Dispatcher, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#Импорт файлов
from script import script
from define import define
from get_netschool import Lessons
from KeyBoards import inline, reply
from config import BOT_TOKEN, GROUP_ADMIN
from state import HelpForm, UserForm
from search_school import search_school
from DataBase.database import db_connect, users

#Обработчик
dp = Dispatcher()

#URL электронного дневника по умолчанию (Кострома)
URL = 'https://netschool.eduportal44.ru/'

#Обработчики бота
@dp.message(F.text == '/start')
async def command_start_handler(message: Message) -> None:
    elements = await users.get_not_empty(message.chat.id)
    if len(elements) != 6:
        await message.answer('Здравствуйте!', reply_markup=reply.no_reg_main)
        await message.answer('Это Telegram бот для работы\n'
                        'с электронным дневником\n\n'
                        'Бот умеет:\n'
                        '1️⃣ Отслеживать ваши оценки\n'
                        '2️⃣ Составлять итоговые результаты\n'
                        '3️⃣ Отображать расписание\n\n'
                        'Чтобы пользоваться ботом вам\n'
                        'необходимо зарегистрироваться,\n'
                        'указав данные вашего дневника', reply_markup=inline.start_0)
    else:
        await message.answer('Здравствуйте!', reply_markup=reply.no_reg_main)
        await message.answer('Это Telegram бот для работы\n'
                        'с электронным дневником\n\n'
                        'Бот умеет:\n'
                        '1️⃣ Отслеживать ваши оценки\n'
                        '2️⃣ Составлять итоговые результаты\n'
                        '3️⃣ Отображать расписание\n\n'
                        'Вы уже зарегистрированы', reply_markup=reply.main)

#Отслеживание inline callback
@dp.callback_query(F.data.in_({'reg'}))
async def callback_reg_handler(call: CallbackQuery, state: FSMContext) -> None:
    elements = await users.get_not_empty(call.message.chat.id)
    if len(elements) == 6:
        await call.message.answer('Вы уже зарегистрированы')
    else:
        await state.clear()
        await call.message.answer('Введите логин', reply_markup=reply.break_reg)
        await users.get_user_id(call.message.chat.id)
        await state.set_state(UserForm.login)

@dp.callback_query(F.data.in_({'user_form_login'}))
async def callback_user_form_login_handler(call: CallbackQuery, state: FSMContext) -> None:
    elements = await users.get_not_empty(call.message.chat.id)
    if len(elements) != 6:
        await call.message.answer("Введите логин")
        await state.set_state(UserForm.login)

@dp.callback_query(F.data.in_({'user_form_password'}))
async def callback_user_form_password_handler(call: CallbackQuery, state: FSMContext) -> None:
    elements = await users.get_not_empty(call.message.chat.id)
    if len(elements) != 6:
        await call.message.answer("Введите пароль")
        await state.set_state(UserForm.password)

@dp.callback_query(F.data.in_({'user_form_num_class'}))
async def callback_user_form_num_class_handler(call: CallbackQuery, state: FSMContext) -> None:
    elements = await users.get_not_empty(call.message.chat.id)
    if len(elements) != 6:
        await call.message.answer("Введите номер класса (например 9)")
        await state.set_state(UserForm.num_class)

@dp.callback_query(F.data.in_({'user_form_search_school_no'}))
async def callback_user_form_search_school_no_handler(call: CallbackQuery, state: FSMContext) -> None:
    elements = await users.get_not_empty(call.message.chat.id)
    if len(elements) != 6:
        await call.message.answer("Введите название школы")
        await state.set_state(UserForm.search_school)

@dp.callback_query(F.data.in_({'user_form_search_school_yes'}))
async def callback_user_form_search_school_yes_handler(call: CallbackQuery, state: FSMContext) -> None:
    elements = await users.get_not_empty(call.message.chat.id)
    if len(elements) != 6:
        msg = await call.message.edit_text("Выполняется подключение...")
        try:
            await users.enter(call.message.chat.id, ['ver', 1])
            user_id, login, password, num_class, name_school, ver = await users.get_not_empty(call.message.chat.id)
            await Lessons.get_data(user_id, login, password, name_school, URL)
            await msg.edit_text('Подключение установленно!\n'
                                'Теперь вы будете получать оповещения\n'
                                'об изменениях в вашем дневнике')
            await call.message.answer('Ещё вы можете воспользоваться\n'
                                      'дополнительными функциями в меню\n'
                                      'над клавиатурой', reply_markup=reply.main)
        except:
            await msg.edit_text('Подключение не удалось! Проверьте\n'
                                'корректность данных и попробуйте заново', 
                                reply_markup=inline.start_0)
            await users.remove(call.message.chat.id)
        await state.clear()

@dp.callback_query(F.data.in_({'help'}))
async def callback_help_handler(call: CallbackQuery) -> None:
    await call.message.edit_text('Вы можете обратиться к\n'
                         'админимтратору, либо найти ответы\n'
                         'на самые популярные вопросы тут:\n\n'
                         '1️⃣ Не находит школу\n'
                         '- Попробуйте использовать название,\n'
                         'указанное на официальном сайте\nшколы\n\n'
                         '2️⃣ Дублирует сообщение об оценке\n'
                         '- О таком случае сообщите\nадминистратору\n\n'
                         'Если у вас ещё остались вопросы, вы\n'
                         'можете обратиться к администратору', reply_markup=inline.help_0)

@dp.callback_query(F.data.in_({'help_input'}))
async def callback_help_input_handler(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text('Введите обращение')
    await state.set_state(HelpForm.help_input)

@dp.callback_query(F.data.in_({'help_input_yes'}))
async def callback_help_input_yes_handler(call: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await bot.forward_message(chat_id=GROUP_ADMIN, from_chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.message.edit_text('Обращение отправленно')
    await state.clear()
    elements = await users.get_not_empty(call.message.chat.id)
    if len(elements) != 6:
        await call.message.answer('Вы можете зарегистрироваться в боте,\n'
                                  'либо обратиться за помощью', reply_markup=inline.start_0)

@dp.callback_query(F.data.in_({'help_input_no'}))
async def callback_help_input_no_handler(call: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await call.message.edit_text('Обращение отменено')
    await state.clear()
    elements = await users.get_not_empty(call.message.chat.id)
    if len(elements) != 6:
        await call.message.answer('Вы можете зарегистрироваться в боте,\n'
                                  'либо обратиться за помощью', reply_markup=inline.start_0)

@dp.callback_query(F.data.in_({'remove_data'}))
async def remove_user_data(call: CallbackQuery) -> None:
    elements = await users.get_not_empty(call.message.chat.id)
    if len(elements) == 6:
        await users.remove(call.message.chat.id)
        await Lessons.remove(call.message.chat.id)
    await call.message.edit_text('Ваши данные полностью удаленны')
    await call.message.answer('Вы всегда можете возобновить работу бота', reply_markup=reply.no_reg_main)
    await call.message.answer('Если у вас возникли трудности\nобратитесь за помощью к\nадминистратору', reply_markup=inline.start_0)

#Обработка состояний
@dp.message(UserForm.login)
async def user_form_login(message: Message, state: FSMContext) -> None:
    elements = await users.get_not_empty(message.chat.id)
    if len(elements) != 6:
        await message.answer(f"Ваш логин: {message.text}", reply_markup=inline.user_form_login)
        await users.enter(message.chat.id, ['login', message.text])
        await message.answer("Введите пароль")
        await state.set_state(UserForm.password)

@dp.message(UserForm.password)
async def user_form_password(message: Message, state: FSMContext) -> None:
    elements = await users.get_not_empty(message.chat.id)
    if len(elements) != 6:
        await message.answer(f"Ваш пароль: {message.text}", reply_markup=inline.user_form_password)
        await users.enter(message.chat.id, ['pass', message.text])
        await message.answer("Введите номер класса (например 9)")
        await state.set_state(UserForm.num_class)

@dp.message(UserForm.num_class)
async def user_form_num_class(message: Message, state: FSMContext) -> None:
    elements = await users.get_not_empty(message.chat.id)
    if len(elements) != 6:
        num_class = re.findall('\d+', message.text)
        if num_class == []: num_class = ['1']
        await message.answer(f"Номер класса: {num_class[0]}", reply_markup=inline.user_form_num_class)
        await users.enter(message.chat.id, ['num_class', num_class[0]])
        await message.answer("Введите название школы")
        await state.set_state(UserForm.search_school)

@dp.message(UserForm.search_school)
async def user_form_search_school(message: Message, state: FSMContext) -> None:
    elements = await users.get_not_empty(message.chat.id)
    if len(elements) != 6:
        try:
            school = search_school(message.text, URL)
            await message.answer(f"{school}\nВаша школа?", reply_markup=inline.user_form_search_school)
            await users.enter(message.chat.id, ['name_school', school])
        except:
            school = 'Такой школы не нашлось'
            await message.answer(f"{school}", reply_markup=inline.user_form_not_search)

@dp.message(HelpForm.help_input)
async def help_form_input(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.answer(f'Отправить обращение:\n{message.text}', reply_markup=inline.help_1)

#
#
#
@dp.callback_query(F.data.in_({'отчёты'}))
async def callback_reports_message(call: CallbackQuery) -> None:
    elements = await users.get_not_empty(call.message.chat.id)
    if len(elements) != 6:
        await call.message.answer("Вы не зарегистрированы", reply_markup=inline.start_0)
    else:
        await call.message.edit_text('Вы можете выбрать тип отчета', reply_markup=inline.reports)

#
#
#
@dp.callback_query(F.data.in_({'итоги', 'итоги 1 полугодие', 'итоги 2 полугодие', 'итоги 1 четверть', 'итоги 2 четверть', 'итоги 3 четверть', 'итоги 4 четверть'}))
async def callback_reports2_message(call: CallbackQuery) -> None:
    elements = await users.get_not_empty(call.message.chat.id)
    if len(elements) != 6:
        await call.message.answer("Вы не зарегистрированы", reply_markup=inline.start_0)
    else:
        time = str(datetime.datetime.now().year)+', '+str(datetime.datetime.now().month)+', '+str(datetime.datetime.now().day)
        s = ''
        if call.data == 'итоги': 
            user_id, login, password, num_class, name_school, ver = await users.get_not_empty(call.message.chat.id)
            s = define(time, num_class)
        year = (await Lessons.get_year(call.message.chat.id))
        if ('полугодие' in s) or ('полугодие' in call.data):
            if s == '':
                s = str(call.data)[6] + ' полугодие'
            index = year.find('2024, 1, 10')
            if s[0] == '1':
                if index == -1:
                    index = len(year)
                year = year[:index]
            else:
                year = year[index:]
            mk = inline.reports1
        elif ('четверть' in s) or ('четверть' in call.data):
            if s == '':
                s = str(call.data)[6] + ' четверть'
            index1 = year.find('2023, 9, 1'), year.find('2023, 10, 25')
            index2 = year.find('2023, 11, 7'), year.find('2023, 12, 29')
            index3 = year.find('2024, 1, 10'), year.find('2024, 2, 22')
            index4 = year.find('2024, 4, 1'), year.find('2024, 5, 28')
            if s[0] == '1':
                year = year[index1[0]:index1[1]]
            elif s[0] == '2':
                year = year[index2[0]:index2[1]]
            elif s[0] == '3':
                year = year[index3[0]:index3[1]]
            else:
                year = year[index4[0]:index4[1]]
            mk = inline.reports2
        mark = {}
        for day in year.split('$'):
            if len(day) > 10:
                day = day[day.index(')')+1:]
                for lesson in day.split('#'):
                    if lesson[2:] in mark.keys():
                        if lesson[0] != '6':
                            mark[lesson[2:]] += lesson[0]
                    else:
                        mark[lesson[2:]] = ''
        result = ''
        for el in mark.keys():
            res = 0
            k = 0
            
            if len(mark.get(el)) < 3:
                res = 'н/а'
            if mark.get(el) == '':
                res = ''
            if mark.get(el) != '' and (len(mark.get(el)) >= 3):
                for i in mark.get(el):
                    res += int(i)
                    k += 1
            if res != 'н/а' and res != '':
                if k != 0:
                    res = res / k
                    if res% 1 >= 0.635:
                        res = int(str(res + 1)[:1])
                    else:
                        res = int(str(res)[:1])
            result += '\n' + el + ': ' + str(res)
        if len(result) < 10:
            result = '\n\nНа данный момент нет результатов'
        if call.message.text != f'📃 Отчет {s}:{result}':
            await call.message.edit_text(f'📃 Отчет {s}:{result}', reply_markup=mk)

#
#
#
@dp.callback_query()
async def otchet(call: CallbackQuery) -> None:
    elements = await users.get_not_empty(call.message.chat.id)
    if len(elements) != 6:
        await call.message.answer("Вы не зарегистрированы", reply_markup=inline.start_0)
    else:
        if 'поурочно' in call.data:
            year = (await Lessons.get_year(call.message.chat.id))
            mark = {}
            for day in year.split('$'):
                if len(day) > 10:
                    day = day[day.index(')')+1:]
                    for lesson in day.split('#'):
                        mark[lesson[2:]] = ''
            for day in year.split('$'):
                if len(day) > 10:
                    time = day[1:day.index(')')] + ' '
                    day = day[day.index(')')+1:]
                    for lesson in day.split('#'):
                        if lesson[0] != '6':
                            mark[lesson[2:]] += lesson[:1] + ' - ' + str(time) + '#'
            i = 0
            for el in mark.keys():
                if i == int(call.data[-2:]):
                    if i+1 == len(mark.keys()):
                        index0 = i-1
                        index1 = 0
                    elif i == 0:
                        index0 = len(mark.keys()) - 1
                        index1 = i+1
                    else:
                        index0 = i-1
                        index1 = i+1
                    data = '\n'.join(mark[el].split('#'))
                    pourochno = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Предыдущий", callback_data=f'поурочно {index0}'), 
                                InlineKeyboardButton(text="Следующий", callback_data=f'поурочно {index1}')
                            ],
                            [
                                InlineKeyboardButton(text="Вернуться", callback_data=f'отчёты')
                            ]
                        ], resize_keyboard=True
                    )
                    el = ' ' + el + ' '
                    while len(el) < 24:
                        el = '~' + el + '~'
                    if len(data) < 3:
                        data = '~ Оценок нет ~\n'
                    await call.message.edit_text(f"{el} \n\n{data}\nУрок - {i+1}", reply_markup=pourochno)
                i += 1
        if ('>' in call.data):
            time = call.data[:-1]
            year = (await Lessons.get_year(call.message.chat.id))
            n = ''
            for day in year.split('$'):
                if len(day) > 10:
                    timecorrect = day[day.index('('):day.index(')')+1]
                    day = day[day.index(')')+1:]
                    if n == time:
                        diary = []
                        for line in day.split('#'):
                            if line[0] in ['1','2','3','4','5']:
                                line = line[2:] + ': ' + line[0]
                            diary.append(line.replace('6 ', ''))
                        diary = '\n'.join(diary)
                        keyboard = InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text="Назад", callback_data=f'{n}<'),
                                    InlineKeyboardButton(text="Вперёд", callback_data=f'{timecorrect}>')
                                ]
                            ], resize_keyboard=True
                        )
                        await call.message.edit_text(f"~ 📗 Дневник на {timecorrect[1:-1]} ~\n{diary}", reply_markup=keyboard)
                        break
                    n = timecorrect
        if ('<' in call.data):
            time = call.data[:-1]
            year = (await Lessons.get_year(call.message.chat.id))
            n = ''
            for day in year.split('$'):
                if len(day) > 10:
                    timecorrect = day[day.index('('):day.index(')')+1]
                    day = day[day.index(')')+1:]
                    if timecorrect == time:
                        diary = []
                        for line in day.split('#'):
                            if line[0] in ['1','2','3','4','5']:
                                line = line[2:] + ': ' + line[0]
                            diary.append(line.replace('6 ', ''))
                        diary = '\n'.join(diary)
                        keyboard = InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text="Назад", callback_data=f'{n}<'),
                                    InlineKeyboardButton(text="Вперёд", callback_data=f'{timecorrect}>')
                                ]
                            ], resize_keyboard=True
                        )
                        await call.message.edit_text(f"~ 📗 Дневник на {timecorrect[1:-1]} ~\n{diary}", reply_markup=keyboard)
                        break
                    n = timecorrect

#Отслеживание reply кнопок
#
# Отслеживание дневника нужно оптимизировать
#
@dp.message(F.text == 'Дневник')
async def diary(message: Message) -> None:
    elements = await users.get_not_empty(message.chat.id)
    if len(elements) != 6:
        await message.answer("Вы не зарегистрированы", reply_markup=inline.start_0)
    else:
        send_time = ''
        time1 = '(' + str(datetime.datetime.now().year) + ', ' + str(datetime.datetime.now().month) + ', ' + str(datetime.datetime.now().day) + ')'
        time = ((datetime.datetime.now().year)*366*12*31) + ((datetime.datetime.now().month)*12*31) + (datetime.datetime.now().day)
        year = await Lessons.get_year(message.chat.id)
        for day in year.split('$'):
            n = send_time
            if len(day) > 10:
                timecorrect1 = day[day.index('(')+1:day.index(')')]
                timecorrect = timecorrect1.split(', ')
                timecorrect1 = '(' + timecorrect1 + ')'
                timecorrect = (int(timecorrect[0])*366*12*31) + (int(timecorrect[1])*12*31) + int(timecorrect[2])
                day = day[day.index(')')+1:]
                if timecorrect == time:
                    diary = []
                    for line in day.split('#'):
                        if line[0] in ['1','2','3','4','5']:
                            line = line[2:] + ': ' + line[0]
                        diary.append(line.replace('6 ', ''))
                    diary = '\n' + '\n'.join(diary)
                    keyboard = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Назад", callback_data=f'{n}<'),
                                InlineKeyboardButton(text="Вперёд", callback_data=f'{timecorrect1}>')
                            ]
                        ], resize_keyboard=True
                    )
                    await message.answer(f"~ 📗 Дневник на {time1[1:-1]} ~{diary}", reply_markup=keyboard)
                    break
                elif timecorrect > time:
                    diary = []
                    for line in day.split('#'):
                        if line[0] in ['1','2','3','4','5']:
                            line = line[2:] + ': ' + line[0]
                        diary.append(line.replace('6 ', ''))
                    diary = '\n' + '\n'.join(diary)
                    keyboard = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text="Назад", callback_data=f'{n}<'),
                                InlineKeyboardButton(text="Вперёд", callback_data=f'{timecorrect1}>')
                            ]
                        ], resize_keyboard=True
                    )
                    await message.answer(f"~ 📗 Дневник на {timecorrect1[1:-1]} ~{diary}", reply_markup=keyboard)
                    break
                else:
                    diary = []
                    for line in day.split('#'):
                        if line[0] in ['1','2','3','4','5']:
                            line = line[2:] + ': ' + line[0]
                        diary.append(line.replace('6 ', ''))
                    diary = '\n'.join(diary)
                    send_time = timecorrect1
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Назад", callback_data=f'{n}<'),
                        InlineKeyboardButton(text="Вперёд", callback_data=f'{send_time}>')
                    ]
                ], resize_keyboard=True
            )
            await message.answer(f"~ 📗 Дневник на {send_time[1:-1]} ~\n{diary}", reply_markup=keyboard)

@dp.message(F.text == 'Отчёты')
async def reports_message(message: Message) -> None:
    elements = await users.get_not_empty(message.chat.id)
    if len(elements) != 6:
        await message.answer("Вы не зарегистрированы", reply_markup=inline.start_0)
    else:
        await message.answer("Вы можете выбрать тип отчета", reply_markup=inline.reports)

@dp.message(F.text == 'Дополнительно')
async def additionally(message: Message) -> None:
    elements = await users.get_not_empty(message.chat.id)
    if len(elements) != 6:
        await message.answer('Вы можете зарегистрироваться\n'
                             'в боте, либо обратиться за\nпомощью', reply_markup=inline.start_0)
    else:
        await message.answer('Вы можете удалить свои\n'
                            'данные из бота, либо\n'
                            'обратиться за помощью', reply_markup=inline.additionally)

@dp.message(F.text == 'Прекратить регистрацию')
async def break_reg(message: Message, state: FSMContext) -> None:
    await message.answer('Регистрация прекращена', reply_markup=reply.no_reg_main)
    await message.answer('Вы можете зарегистрироваться в боте,\n'
                         'либо обратиться за помощью', 
                         reply_markup=inline.start_0)
    await state.clear()

#Запуск бота
async def main() -> None:
    db_connect()
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    polling = asyncio.create_task(dp.start_polling(bot, skip_updates=True))
    listen = asyncio.create_task(script())
    await polling
    await listen

if __name__ == "__main__":
    asyncio.run(main())