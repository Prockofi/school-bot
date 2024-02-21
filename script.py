import asyncio
from aiogram import Bot
from get_netschool import Lessons
from DataBase.database import users as db
from config import BOT_TOKEN

#URL электронного дневника по умолчанию (Кострома)
URL = 'https://netschool.eduportal44.ru/'

async def script() -> None:
    print('Скрипт запущен')
    while True:
        users = await db.get()
        if len(users) != 0: 
            for user in users:
                if not (None in user):
                    try:
                        user_id, login, password, num_class, name_school, ver = user[1:]
                        bot = Bot(BOT_TOKEN)
                        (new, old), year = await Lessons.get_data(user_id, login, password, name_school, URL)
                        for i in range(len(new)):
                            if '6 ' in new[i]:
                                new[i] = ''
                        new = '\n' + '\n'.join(new)
                        for i in range(len(old)):
                            if '6 ' in old[i]:
                                old[i] = ''
                        old = '\n' + '\n'.join(old)
                        new = new.replace('\n\n', '\n')
                        old = old.replace('\n\n', '\n')
                        if len(new) > 10:
                            await bot.send_message(user_id, f'Новые оценки:{new}')
                        if len(old) > 10:
                            await bot.send_message(user_id, f'Эти оценки удалили:{old}')
                    except:
                        print('Ошибка 1')
        await asyncio.sleep(1200)