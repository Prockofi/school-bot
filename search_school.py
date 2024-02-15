import requests, json

#Принимает название школы и url электронного дневника
def search_school(name_school: str, url: str) -> str:
    responce = requests.get(f'{url}/webapi/schools/search').json()
    res = []
    name_school = (name_school.replace('№', '№ ')).split()
    while '  ' in name_school:
        name_school = name_school.replace('  ', ' ')
    for word in name_school:
        try: 
            num = int(word)
            break
        except:
            pass
    else:
        num = None
    for word in name_school:
        for line in responce:
            if word.lower() in line['name'].lower():
                res.append(line['shortName'])
    schools = ''
    max_count = 0
    for el in res:
        if res.count(el) > max_count:
            if num != None:
                if str(num) in el:
                    max_count = res.count(el)
                    school = el
            else:
                max_count = res.count(el)
                school = el
    return school