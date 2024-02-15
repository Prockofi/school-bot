import asyncio, datetime
from netschoolapi import NetSchoolAPI
from DataBase.database import lessons

class LessonsClass:
    async def main(self, login: str, password: str, school: str, school_url: str) -> str:
        connect = NetSchoolAPI(school_url)
        await connect.login(login, password, school)
        get_data = await connect.diary(start=datetime.date(2023, 9, 1), end=datetime.date(2024, 5, 31))
        await connect.logout()

        get_data = str(get_data).split('Day')
        year = {}
        for get_day in get_data:
            day = []
            for el in get_day.split('Lesson('):
                if len(str(el)) > 10:
                    line = ''
                    index = el.find(', mark=')
                    if el.count('mark') == 2 and (el[index+7:index+8] in 'N')  and (el[index+7:index+8] != ''):
                        index = el.find(', mark=', index+50)
                    if index != -1:
                        if (el[index+7:index+8] in ['1', '2', '3', '4', '5']) and (el[index+7:index+8] != ''):
                            line += el[index+7:index+8]
                        else:
                            line += '6'
                    else:
                        line = '6' + line
                    index = el.find('subject=')
                    if index != -1:
                        lesson = el[index+8:index+40].split("'")
                        line += ' ' + lesson[1]
                    index = el.find('day=datetime.date(')
                    if index != -1:
                        if ', ' == el[index+29:index+31]:
                            time = el[index+17:index+29]
                        elif ',' == el[index+30:index+31]:
                            time = el[index+17:index+30]
                        else:
                            time = el[index+17:index+31]
                    day.append(line)
                if len(str(day)) > 10:
                    year[time] = day
        write_data = ''
        for day in year.keys():
            write_data += '$' + day + '#'.join(year.get(day))
        return str(write_data)

    async def get_data(self, user_id: int, login: str, password: str, school: str, school_url: str) -> list:
        year = await self.main(login, password, school, school_url)
        try:
            read_data = (await lessons.get_not_empty(user_id))[1]
        except:
            read_data = 'None'
        await lessons.get_user_id(user_id)
        await lessons.enter(user_id, ['lessons', year])
        return await self.compare((await self.filter(year)).split('#'), (await self.filter(read_data)).split('#')), year

    async def compare(self, new_data: str, old_data: str) -> list:
        new_mark, old_mark = [], []
        for el in new_data:
            if not (el in old_data):
                new_mark.append(el)
        for el in old_data:
            if not (el in new_data):
                old_mark.append(el)
        return new_mark, old_mark

    async def filter(self, data: str) -> str:
        marks = ''
        for day in data.split('$'):
            if len(str(day)) > 10:
                try:
                    time = day[day.index('('):day.index(')')+1]
                    for mark in day[day.index(')')+1:].split('#'):
                        marks += '#' + mark + ' ' + time
                except:
                    pass
        return marks

    async def get_year(self, user_id: int) -> str:
        less = await lessons.get_not_empty(user_id)
        if less:
            return less[1]

    async def remove(self, user_id: int) -> None:
        await lessons.remove(user_id)

Lessons = LessonsClass()