import sqlite3

def db_connect() -> None:
    global db, cur
    db = sqlite3.connect("/home/prockofi/schoolbot/DataBase/bot.db")
    cur = db.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "user_id INTEGER,"
        "login TEXT,"
        "pass TEXT,"
        "num_class INT,"
        "name_school TEXT,"
        "ver INTEGER)"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS lessons(id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "user_id INTEGER,"
        "lessons TEXT)"
    )
    db.commit()

# БД
class DataBase:
    def __init__(self, name: str):
        self.name = name

    async def user_id(self, user_id: int) -> None:
        user = cur.execute(f"""SELECT * FROM {self.name} WHERE user_id == ?""", (user_id, )).fetchone()
        if not user:
            cur.execute(f"""INSERT INTO {self.name} (user_id) VALUES (?)""", (user_id, ))
            db.commit()

    async def remove(self, user_id: int) -> None:
        user = cur.execute(f"""SELECT * FROM {self.name} WHERE user_id = ?""", (user_id, )).fetchone()
        if user:
            user = cur.execute(f"""DELETE FROM {self.name} WHERE user_id = ?""", (user_id, )).fetchone()
            db.commit()

    async def enter(self, user_id: int, fields: list) -> None:
        user = cur.execute(f"""SELECT * FROM {self.name} WHERE user_id == ?""", (user_id, )).fetchone()
        if user:
            cur.execute(f"""UPDATE {self.name} SET {fields[0]} = ? WHERE user_id = ?""", (fields[1], user_id))
            db.commit()

    async def get_not_empty(self, user_id: int) -> list:
        user = cur.execute(f"""SELECT * FROM {self.name} WHERE user_id == ?""", (user_id, )).fetchone()
        if user:
            result = []
            for val in user[1:]:
                if not val == None:
                    result.append(val)
            return result
        else:
            return ''

    async def get(self) -> list:
        users = cur.execute(f"""SELECT * FROM {self.name}""").fetchall()
        return users

users = DataBase("users")
lessons = DataBase("lessons")