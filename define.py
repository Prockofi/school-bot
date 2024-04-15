import datetime

now_year = ["2023", "2024"]
periods = [
    {"1 четверть":f"{now_year[0]}, 9, 1:{now_year[0]}, 10, 27", 
    "2 четверть":f"{now_year[0]}, 10, 28:{now_year[0]}, 12, 29", 
    "3 четверть":f"{now_year[1]}, 1, 1:{now_year[1]}, 3, 22", 
    "4 четверть":f"{now_year[1]}, 3, 23:{now_year[1]}, 5, 28"},
    {"1 полугодие":f"{now_year[0]}, 9, 1:{now_year[0]}, 12, 29", 
    "2 полугодие":f"{now_year[1]}, 1, 1:{now_year[1]}, 5, 28"}
]

#
#
#
def define(num_class: int) -> str:
    if num_class > 9:
        period = periods[1]
    else:
        period = periods[0]
    for quarter in period.keys():
        time_start, time_end = period.get(quarter).split(':')
        time_start, time_end = time_start.split(', '), time_end.split(', ')
        time_start = int(time_start[0])*366 + int(time_start[1])*31 + int(time_start[2])
        time_end = int(time_end[0])*366 + int(time_end[1])*31 + int(time_end[2])

        time_now = datetime.datetime.now().year*366 + datetime.datetime.now().month*31 + datetime.datetime.now().day
        if time_start <= time_now <= time_end:
            return quarter

#
#
#
def define_year(period: str, year: str) -> str:
    k = 0
    if "полугодие" in period:
        if period[0] == '1':
            start = "$(" + (periods[1].get("1 полугодие").split(':')[1]) + ')'
            end = 0
            index_start = year.find(start)
            while index_start == -1 and k < 30:
                start, end = redefine_year(start, end, '>')
                index_start = year.find(start)
                k += 1
            return year[:index_start]
        else:
            start = "$(" + (periods[1].get("2 полугодие").split(':')[0]) + ')'
            end = 0
            index_start = year.find(start)
            while index_start == -1 and k < 30:
                start, end = redefine_year(start, end, '>')
                index_start = year.find(start)
                k += 1
            return year[index_start:]
    else:
        if period[0] == '1':
            start = "$(" + (periods[0].get("1 четверть").split(':')[1]) + ')'
            end = 0
            index_start = year.find(start)
            while index_start == -1 and k < 30:
                start, end = redefine_year(start, end, '>')
                index_start = year.find(start)
                k += 1
            return year[:index_start]
        elif period[0] == '2':
            start = "$(" + (periods[0].get("2 четверть").split(':')[0]) + ')'
            end = "$(" + (periods[0].get("2 четверть").split(':')[1]) + ')'
            index_start = year.find(start)
            while index_start == -1 and k < 30:
                start, end = redefine_year(start, end, '>')
                index_start = year.find(start)
                k += 1
            index_end = -1
            while index_end == -1 and k < 30:
                end, start = redefine_year(end, start, '>')
                index_end = year.find(end)
                k += 1
            return year[index_start:index_end]
        elif period[0] == '3':
            start = "$(" + (periods[0].get("3 четверть").split(':')[0]) + ')'
            end = "$(" + (periods[0].get("3 четверть").split(':')[1]) + ')'
            index_start = year.find(start)
            while index_start == -1 and k < 30:
                start, end = redefine_year(start, end, '>')
                index_start = year.find(start)
                k += 1
            index_end = -1
            while index_end == -1 and k < 30:
                end, start = redefine_year(end, start, '>')
                index_end = year.find(end)
                k += 1
            return year[index_start:index_end]
        else:
            start = '$(' + (periods[0].get('4 четверть').split(':')[0]) + ')'
            end = 0
            index_start = year.find(start)
            while index_start == -1 and k < 30:
                start, end = redefine_year(start, end, '>')
                index_start = year.find(start)
                k += 1
            return year[index_start:]

#
#
#
def redefine_year(index_start: str, index_end: str, vect: str) -> str:
    i1, i2, i3 = index_start[2:-1].split(', ')
    if vect == '<':
        if int(i3) > 1:
            i3 = int(i3) - 1
        else:
            if int(i2) > 1:
                i2 = int(i2) - 1
                i3 = 31
            else:
                i1 = int(i1) - 1
                i2 = 12
                i3 = 31
    else:
        if int(i3) < 31:
            i3 = int(i3) + 1
        else:
            if int(i2) < 12:
                i2 = int(i2) + 1
                i3 = 1
            else:
                i1 = int(i1) + 1
                i2 = 1
                i3 = 1
    index_start = f'$({i1}, {i2}, {i3})'
    return index_start, index_end