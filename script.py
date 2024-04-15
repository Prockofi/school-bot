import asyncio
from config import URL
from get_netschool import Lessons
from DataBase.database import users as db

async def script(bot) -> None:
    while True:
        users = await db.get()
        if len(users) != 0: 
            for user in users:
                if None not in user:
                    try:
                        user_id, login, password, num_class, name_school, ver = user[1:]
                        (new, old), year = await Lessons.get_data(user_id, login, password, name_school, URL)
                        for i in range(len(new)):
                            if "6 " in new[i]:
                                new[i] = ''
                        new = '\n' + '\n'.join(new)
                        for i in range(len(old)):
                            if "6 " in old[i]:
                                old[i] = ''
                        old = "\n" + '\n'.join(old)
                        new = new.replace("\n\n", "\n")
                        old = old.replace("\n\n", "\n")
                        if (('1' in new) or ('2' in new) or ('3' in new) or ('4' in new) or ('5' in new)):
                            await bot.send_message(user_id, f"Новые оценки:{new}")
                        if (('1' in old) or ('2' in old) or ('3' in old) or ('4' in old) or ('5' in old)):
                            await bot.send_message(user_id, f"Эти оценки удалили:{old}")
                    except:
                        print("Ошибка в скрипте")
        await asyncio.sleep(900) #900 sec - 15 min