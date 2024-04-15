from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_no_reg = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Зарегистрироваться", callback_data="reg")
        ],
        [
            InlineKeyboardButton(text="Помочь", callback_data="help")
        ]
    ], resize_keyboard=True
)

help_0 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Написать обращение администратору", callback_data="help_input")
        ]
    ], resize_keyboard=True
)

help_1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="help_input_yes"),
            InlineKeyboardButton(text="Нет", callback_data="help_input_no")
        ]
    ], resize_keyboard=True
)

user_form_login = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить", callback_data="user_form_login")
        ]
    ], resize_keyboard=True
)

user_form_password = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить", callback_data="user_form_password")
        ]
    ], resize_keyboard=True
)

user_form_num_class = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить", callback_data="user_form_num_class")
        ]
    ], resize_keyboard=True
)

user_form_search_school = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="user_form_search_school_yes"),
            InlineKeyboardButton(text="Нет", callback_data="user_form_search_school_no")
        ]
    ], resize_keyboard=True
)

user_form_not_search = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Выбрать другую", callback_data=f"user_form_search_school_no")
        ]
    ], resize_keyboard=True
)

additionally = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Удалить", callback_data="remove_user_data")
        ],
        [
            InlineKeyboardButton(text="Помочь", callback_data="help")
        ]
    ], resize_keyboard=True
)

reports = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Итоги", callback_data="итоги"), 
            InlineKeyboardButton(text="Итоги поурочно", callback_data="поурочно 0")
        ]
    ], resize_keyboard=True
)

reports1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1 полугодие", callback_data=f"итоги 1 полугодие"),
            InlineKeyboardButton(text="2 полугодие", callback_data=f"итоги 2 полугодие")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data=f"отчёты")
        ]
    ], resize_keyboard=True
)

reports2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1 чет", callback_data=f"итоги 1 четверть"),
            InlineKeyboardButton(text="2 чет", callback_data=f"итоги 2 четверть"),
            InlineKeyboardButton(text="3 чет", callback_data=f"итоги 3 четверть"),
            InlineKeyboardButton(text="4 чет", callback_data=f"итоги 4 четверть")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data=f"отчёты")
        ]
    ], resize_keyboard=True
)