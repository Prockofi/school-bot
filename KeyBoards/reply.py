from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Отчёты"), 
        KeyboardButton(text="Дневник")
    ],
    [
        KeyboardButton(text="Дополнительно")
    ]  
    ], resize_keyboard=True
)

start_no_reg = ReplyKeyboardMarkup(
    keyboard=[
    [
        KeyboardButton(text="Дополнительно")
    ]  
    ], resize_keyboard=True
)

break_reg = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Прекратить регистрацию")
    ]
    ], resize_keyboard=True
)
