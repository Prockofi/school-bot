def define(time: str, num_class: int) -> str:
    if num_class <= 9:
        s = {'1 четверть':'2023, 9, 1:2023, 10, 27', '2 четверть':'2023, 11, 6:2023, 12, 29', '3 четверть':'2024, 1, 10:2024, 2, 22', '4 четверть':'2024, 4, 1:2024, 5, 28'}
    else:
        s = {'1 полугодие':'2023, 9, 1:2023, 12, 29', '2 полугодие':'2024, 1, 10:2024, 5, 28'}
    for quarter in s.keys():
        t1, t2 = s.get(quarter).split(':')
        t1, t2 = t1.split(', '), t2.split(', ')
        t1 = int(t1[0])*366 + int(t1[1])*31 + int(t1[2])
        t2 = int(t2[0])*366 + int(t2[1])*31 + int(t2[2])

        t3 = time.split(', ')
        t3 = int(t3[0])*366 + int(t3[1])*31 + int(t3[2])
        if t3 >= t1 and t3 <= t2:
            return quarter