# Испорт библиотек
import asyncio, sys
from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackQuery

# Доп. импорт
from config import TOKEN

#Обработчик
disp = Dispatcher()

date = sys.argv[1]
#
# Сообщение о временных работах
#
@disp.message()
async def messege_get(message: Message) -> None:
    await message.answer(f"В данный момент ведутся\nработы по обновлению бота.\nБот восстановит свою работу\nне позже {date}.")

@disp.callback_query()
async def callback_get(call: CallbackQuery) -> None:
    await call.message.answer(f"В данный момент ведутся\nработы по обновлению бота.\nБот восстановит свою работу\nне позже {date}.")

#Запуск бота
async def main() -> None:
    bot = Bot(TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await disp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
