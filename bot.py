# Испорт библиотек
import asyncio, datetime, re
from aiogram import Dispatcher, F, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackQuery

# Доп. импорт
from script import script
from config import TOKEN, ADMIN_GROUP, URL
from state import HelpForm, UserForm
from DataBase.database import db_connect, users
from Keyboards import reply, inline
from define import define, define_year
from get_netschool import Lessons
from search_school import search_school

#Обработчик
disp = Dispatcher()

#
# Обработчики команд
#
@disp.message(F.text == "/start")
async def command_start_handler(message: Message) -> None:
    REG = len(await users.get_not_empty(message.chat.id)) == 6
    if not REG:
        await message.answer("Здравствуйте!", reply_markup=reply.start_no_reg)
        await message.answer("Это Telegram бот для работы\n"
                        "с электронным дневником\n\n"
                        "Бот умеет:\n"
                        "1️⃣ Отслеживать ваши оценки\n"
                        "2️⃣ Составлять итоговые результаты\n"
                        "3️⃣ Отображать расписание\n\n"
                        "Чтобы пользоваться ботом вам\n"
                        "необходимо зарегистрироваться,\n"
                        "указав данные вашего дневника", reply_markup=inline.start_no_reg)
    else:
        await message.answer("Здравствуйте!", reply_markup=reply.start)
        await message.answer("Это Telegram бот для работы\n"
                        "с электронным дневником\n\n"
                        "Бот умеет:\n"
                        "1️⃣ Отслеживать ваши оценки\n"
                        "2️⃣ Составлять итоговые результаты\n"
                        "3️⃣ Отображать расписание\n\n"
                        "Вы уже зарегистрированы")

@disp.message(F.text == "/help")
async def command_help_handler(message: Message) -> None:
    await message.answer("Вы можете обратиться к\n"
                         "админимтратору, либо найти ответы\n"
                         "на популярные вопросы тут:\n\n"
                         "1️⃣ Не находит школу\n"
                         "- Попробуйте использовать название, "
                         "указанное на официальном сайте школы\n\n"
                         "Если у вас ещё остались вопросы,\n"
                         "вы можете обратиться к администратору", reply_markup=inline.help_0)

#
# Обработчики текста
#
@disp.message(F.text == "Прекратить регистрацию")
async def break_reg(message: Message, state: FSMContext) -> None:
    await message.answer("Регистрация прекращена",
                         reply_markup=reply.start_no_reg)
    await message.answer("Вы можете зарегистрироваться\n"
                         "в боте, либо обратиться за\nпомощью", reply_markup=inline.start_no_reg)
    await state.clear()

@disp.message(F.text == "Дополнительно")
async def additionally(message: Message) -> None:
    REG = len(await users.get_not_empty(message.chat.id)) == 6
    if not REG:
        await message.answer("Вы можете зарегистрироваться\n"
                             "в боте, либо обратиться за\nпомощью", reply_markup=inline.start_no_reg)
    else:
        await message.answer("Вы можете удалить свои\n"
                            "данные из бота, либо\n"
                            "обратиться за помощью", reply_markup=inline.additionally)

@disp.message(F.text == "Отчёты")
async def reports_message(message: Message) -> None:
    REG = len(await users.get_not_empty(message.chat.id)) == 6
    if not REG:
        await message.answer("Вы можете зарегистрироваться\n"
                             "в боте, либо обратиться за\nпомощью", reply_markup=inline.start_no_reg)
    else:
        await message.answer("Вы можете выбрать тип отчёта", reply_markup=inline.reports)

@disp.message(F.text == "Дневник")
async def diary(message: Message) -> None:
    elements = await users.get_not_empty(message.chat.id)
    if len(elements) != 6:
        await message.answer("Вы можете зарегистрироваться\n"
                             "в боте, либо обратиться за\nпомощью", reply_markup=inline.start_no_reg)
    else:
        time1 = '(' + str(datetime.datetime.now().year) + ', ' + str(datetime.datetime.now().month) + ', ' + str(datetime.datetime.now().day) + ')'
        time = ((datetime.datetime.now().year)*366*12*31) + ((datetime.datetime.now().month)*12*31) + (datetime.datetime.now().day)
        year = await Lessons.get_year(message.chat.id)
        for day in year.split('$'):
            if len(day) > 10:
                last_time = '(' + day[day.index('(')+1:day.index(')')] + ')'
                timecorrect = last_time[1:-1].split(', ')
                timecorrect = (int(timecorrect[0])*366*12*31) + (int(timecorrect[1])*12*31) + int(timecorrect[2])
                if timecorrect >= time:
                    break
        day = day[day.index(')')+1:]
        diary = []
        for line in day.split('#'):
            if line[0] in ['1','2','3','4','5']:
                line = line[2:] + ': ' + line[0]
            diary.append(line.replace("6 ", ''))
        diary = '\n' + '\n'.join(diary)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад", callback_data=f"{last_time}<"),
                    InlineKeyboardButton(text="Вперёд", callback_data=f"{last_time}>")
                ]
            ], resize_keyboard=True
        )
        await message.answer(f"~ 📗 Дневник на {last_time[1:-1]} ~{diary}", reply_markup=keyboard)

#
# Отслеживание inline callback
#
@disp.callback_query(F.data.in_({"reg"}))
async def callback_reg_handler(call: CallbackQuery, state: FSMContext) -> None:
    REG = len(await users.get_not_empty(call.message.chat.id)) == 6
    if REG:
        await call.message.answer("Вы уже зарегистрированы")
    else:
        await call.message.answer("Введите логин", reply_markup=reply.break_reg)
        await users.user_id(call.message.chat.id)
        await state.set_state(UserForm.login)

@disp.callback_query(F.data.in_({"user_form_login"}))
async def callback_user_form_login_handler(call: CallbackQuery, state: FSMContext) -> None:
    REG = len(await users.get_not_empty(call.message.chat.id)) == 6
    if not REG:
        await call.message.answer("Введите логин")
        await state.set_state(UserForm.login)

@disp.callback_query(F.data.in_({"user_form_password"}))
async def callback_user_form_password_handler(call: CallbackQuery, state: FSMContext) -> None:
    REG = len(await users.get_not_empty(call.message.chat.id)) == 6
    if not REG:
        await call.message.answer("Введите пароль")
        await state.set_state(UserForm.password)

@disp.callback_query(F.data.in_({"user_form_num_class"}))
async def callback_user_form_num_class_handler(call: CallbackQuery, state: FSMContext) -> None:
    REG = len(await users.get_not_empty(call.message.chat.id)) == 6
    if not REG:
        await call.message.answer("Введите номер класса (например 9)")
        await state.set_state(UserForm.num_class)

@disp.callback_query(F.data.in_({"user_form_search_school_no"}))
async def callback_user_form_search_school_no_handler(call: CallbackQuery, state: FSMContext) -> None:
    REG = len(await users.get_not_empty(call.message.chat.id)) == 6
    if not REG:
        await call.message.answer("Попробуйте использовать название\nуказанное на официальном сайте\nшколы")
        await call.message.answer("Введите название школы")
        await state.set_state(UserForm.search_school)

@disp.callback_query(F.data.in_({"user_form_search_school_yes"}))
async def callback_user_form_search_school_yes_handler(call: CallbackQuery, state: FSMContext) -> None:
    REG = len(await users.get_not_empty(call.message.chat.id)) == 6
    if not REG:
        msg = await call.message.edit_text("Выполняется подключение...")
        try:
            user_id, login, password, num_class, name_school = await users.get_not_empty(call.message.chat.id)
            await Lessons.get_data(user_id, login, password, name_school, URL)
            await users.enter(call.message.chat.id, ["ver", 1])
            await msg.edit_text("Подключение установленно!\n"
                                "Теперь вы будете получать оповещения\n"
                                "об изменениях в вашем дневнике")
            await call.message.answer("Ещё вы можете воспользоваться\n"
                                      "дополнительными функциями в меню\n"
                                      "над клавиатурой", reply_markup=reply.start)
        except:
            await msg.edit_text("Подключение не удалось! Проверьте\n"
                                "корректность данных и попробуйте заново", 
                                reply_markup=inline.start_no_reg)
            await users.remove(call.message.chat.id)
        await state.clear()

@disp.callback_query(F.data.in_({"help"}))
async def callback_help_handler(call: CallbackQuery) -> None:
    await call.message.edit_text("Вы можете обратиться к\n"
                         "админимтратору, либо найти ответы\n"
                         "на популярные вопросы тут:\n\n"
                         "1️⃣ Не находит школу\n"
                         "- Попробуйте использовать название, "
                         "указанное на официальном сайте школы\n\n"
                         "Если у вас ещё остались вопросы,\n"
                         "вы можете обратиться к администратору", reply_markup=inline.help_0)

@disp.callback_query(F.data.in_({"help_input"}))
async def callback_help_input_handler(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text("Введите обращение")
    await state.set_state(HelpForm.help_input)

@disp.callback_query(F.data.in_({"help_input_yes"}))
async def callback_help_input_yes_handler(call: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await bot.send_message(chat_id=ADMIN_GROUP, text=f"<code>{call.message.chat.id}</code> - {call.message.chat.first_name}", parse_mode=ParseMode.HTML)
    await bot.send_message(chat_id=ADMIN_GROUP, text=f"{call.message.text}"[21:])
    await call.message.edit_text("Обращение отправленно")
    await state.clear()
    REG = len(await users.get_not_empty(call.message.chat.id)) == 6
    if not REG:
        await message.answer("Вы можете зарегистрироваться\n"
                             "в боте, либо обратиться за\nпомощью", reply_markup=inline.start_no_reg)

@disp.callback_query(F.data.in_({"help_input_no"}))
async def callback_help_input_no_handler(call: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await call.message.edit_text("Обращение отменено")
    await state.clear()
    REG = len(await users.get_not_empty(call.message.chat.id)) == 6
    if not REG:
        await message.answer("Вы можете зарегистрироваться\n"
                             "в боте, либо обратиться за\nпомощью", reply_markup=inline.start_no_reg)

@disp.callback_query(F.data.in_({"remove_user_data"}))
async def remove_user_data(call: CallbackQuery) -> None:
    REG = len(await users.get_not_empty(call.message.chat.id)) == 6
    if REG:
        await users.remove(call.message.chat.id)
        await Lessons.remove(call.message.chat.id)
    await call.message.edit_text("Ваши данные полностью удаленны")
    await call.message.answer("Вы всегда можете возобновить работу бота", reply_markup=reply.start_no_reg)
    await call.message.answer("Если у вас возникли трудности\n"
                              "обратитесь за помощью к\n"
                              "администратору",
                              reply_markup=inline.start_no_reg)

@disp.callback_query(F.data.in_({"отчёты"}))
async def callback_reports_message(call: CallbackQuery) -> None:
    REG = len(await users.get_not_empty(call.message.chat.id)) == 6
    if not REG:
        await message.answer("Вы можете зарегистрироваться\n"
                             "в боте, либо обратиться за\nпомощью", reply_markup=inline.start_no_reg)
    else:
        await call.message.edit_text("Вы можете выбрать тип отчёта", reply_markup=inline.reports)

@disp.callback_query(F.data.in_({"итоги", "итоги 1 полугодие", "итоги 2 полугодие", "итоги 1 четверть", "итоги 2 четверть", "итоги 3 четверть", "итоги 4 четверть"}))
async def callback_reports_1_message(call: CallbackQuery) -> None:
    elements = await users.get_not_empty(call.message.chat.id)
    if len(elements) != 6:
        await message.answer("Вы можете зарегистрироваться\n"
                             "в боте, либо обратиться за\nпомощью", reply_markup=inline.start_no_reg)
    else:
        year = await Lessons.get_year(call.message.chat.id)
        if call.data == "итоги":
            period = define(int(elements[3]))
        else:
            period = str(call.data)[6:]
        if int(elements[3]) > 9:
            kb = inline.reports1
        else:
            kb = inline.reports2
        year = define_year(period, year)
        marks = {}
        for day in year.split('$'):
            if len(day) > 10:
                day = day[day.index(')')+1:]
                for lesson in day.split('#'):
                    if lesson[2:] in marks.keys():
                        if lesson[0] != '6':
                            marks[lesson[2:]] += lesson[0]
                    else:
                        marks[lesson[2:]] = ''
        result = ''
        for el in marks.keys():
            float_res = 0
            if len(marks.get(el)) >= 3:
                res = [int(i) for i in marks.get(el)]
                res = sum(res)/len(res)
                float_res = round(res, 2)
                if res % 1 >= 0.64:
                    res = int(str(res + 1)[:1])
                else:
                    res = int(str(res)[:1])
                result += '\n' + el + ": " + str(res) + ' (' + str(float_res) + ')'
            else:
                result += '\n' + el + ": н/а"
        if len(marks.keys()) == 0:
            result = "\n\nНа данный момент нет результатов"
        if call.message.text != f"📃 Отчёт {period}:{result}":
            await call.message.edit_text(f"📃 Отчёт {period}:{result}", reply_markup=kb)

@disp.callback_query()
async def callback_reports_2_and_diary_message(call: CallbackQuery) -> None:
    elements = await users.get_not_empty(call.message.chat.id)
    if len(elements) != 6:
        await message.answer("Вы можете зарегистрироваться\n"
                             "в боте, либо обратиться за\nпомощью", reply_markup=inline.start_no_reg)
    else:
        year = await Lessons.get_year(call.message.chat.id)
        if "поурочно" in call.data:
            marks = {}
            for day in year.split('$'):
                if len(day) > 10:
                    time = day[1:day.index(')')]
                    day = day[day.index(')')+1:]
                    for lesson in day.split('#'):
                        if lesson[2:] in marks.keys():
                            if lesson[0] != '6':
                                marks[lesson[2:]] += lesson[:1] + " - " + time + '#'
                        else:
                            marks[lesson[2:]] = ''
            i = int(call.data[-2:])
            el = list(marks.keys())[i]
            if i+1 == len(marks.keys()):
                index0 = i-1
                index1 = 0
            elif i == 0:
                index0 = len(marks.keys()) - 1
                index1 = i+1
            else:
                index0 = i-1
                index1 = i+1
            data = '\n'.join(marks[el].split('#'))
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Предыдущий", callback_data=f"поурочно {index0}"), 
                        InlineKeyboardButton(text="Следующий", callback_data=f"поурочно {index1}")
                    ],
                    [
                        InlineKeyboardButton(text="Вернуться", callback_data=f"отчёты")
                    ]
                ], resize_keyboard=True
            )
            el = ' ' + el + ' '
            while len(el) < 24:
                el = '~' + el + '~'
            if not (('1' in data) or ('2' in data) or ('3' in data) or ('4' in data) or ('5' in data)):
                data = "~ Оценок нет ~\n"
            await call.message.edit_text(f"{el}\n\n{data}\nУрок - {i+1}", reply_markup=keyboard)
        else:   
            now_time = call.data[:-1]
            last_time = ''
            for day in year.split('$'):
                if len(day) > 10:
                    next_time = day[day.index('('):day.index(')')+1]
                    if ((last_time == now_time) and ('>' in call.data)) or ((next_time == now_time) and ('<' in call.data)):
                        day = day[day.index(')')+1:]
                        diary = []
                        for line in day.split('#'):
                            if line[0] in ['1','2','3','4','5']:
                                line = line[2:] + ': ' + line[0]
                            diary.append(line.replace("6 ", ''))
                        diary = '\n'.join(diary)
                        keyboard = InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text="Назад", callback_data=f"{last_time}<"),
                                    InlineKeyboardButton(text="Вперёд", callback_data=f"{next_time}>")
                                ]
                            ], resize_keyboard=True
                        )
                        await call.message.edit_text(f"~ 📗 Дневник на {next_time[1:-1]} ~\n{diary}", reply_markup=keyboard)
                        break
                    last_time = next_time

#
# Обработка состояний
#
@disp.message(UserForm.login)
async def user_form_login(message: Message, state: FSMContext) -> None:
    REG = len(await users.get_not_empty(message.chat.id)) == 6
    if not REG:
        await message.answer(f"Ваш логин: {message.text}", reply_markup=inline.user_form_login)
        await users.enter(message.chat.id, ["login", message.text])
        await message.answer("Введите пароль")
        await state.set_state(UserForm.password)

@disp.message(UserForm.password)
async def user_form_password(message: Message, state: FSMContext) -> None:
    REG = len(await users.get_not_empty(message.chat.id)) == 6
    if not REG:
        await message.answer(f"Ваш пароль: {message.text}", reply_markup=inline.user_form_password)
        await users.enter(message.chat.id, ["pass", message.text])
        await message.answer("Введите номер класса (например 9)")
        await state.set_state(UserForm.num_class)

@disp.message(UserForm.num_class)
async def user_form_num_class(message: Message, state: FSMContext) -> None:
    REG = len(await users.get_not_empty(message.chat.id)) == 6
    if not REG:
        num_class = re.findall("\d+", message.text)
        if num_class == []: num_class = ["1"]
        await message.answer(f"Номер класса: {num_class[0]}", reply_markup=inline.user_form_num_class)
        await users.enter(message.chat.id, ["num_class", num_class[0]])
        await message.answer("Введите название школы")
        await state.set_state(UserForm.search_school)

@disp.message(UserForm.search_school)
async def user_form_search_school(message: Message, state: FSMContext) -> None:
    REG = len(await users.get_not_empty(message.chat.id)) == 6
    if not REG:
        school = search_school(message.text.lower(), URL)
        if school != None:
            await message.answer(f"{school}\nВаша школа?", reply_markup=inline.user_form_search_school)
            await users.enter(message.chat.id, ["name_school", school])
        else:
            school = "Такой школы не нашлось"
            await message.answer(f"{school}", reply_markup=inline.user_form_not_search)

@disp.message(HelpForm.help_input)
async def help_form_input(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.answer(f"Отправить обращение:\n{message.text}", reply_markup=inline.help_1)

@disp.callback_query(F.data.in_({"отчёты"}))
async def callback_reports_message(call: CallbackQuery) -> None:
    REG = len(await users.get_not_empty(message.chat.id)) == 6
    if not REG:
        await call.message.answer("Вы не зарегистрированы", reply_markup=inline.start_no_reg)
    else:
        await call.message.edit_text("Вы можете выбрать тип отчёта", reply_markup=inline.reports)

#Запуск бота
async def main() -> None:
    db_connect()
    bot = Bot(TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    polling = asyncio.create_task(disp.start_polling(bot, skip_updates=True))
    sp = asyncio.create_task(script(Bot(TOKEN)))
    await polling
    await sp

if __name__ == "__main__":
    asyncio.run(main())
