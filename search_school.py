import requests, json, re

# Принимает название школы и url электронного дневника
def search_school(name_school: str, url: str) -> str:
    responce = requests.get(f"{url}/webapi/schools/search").json()
    res = []
    name_school = (name_school.replace("№", " № "))
    name_school = (name_school.replace("сош", " сош "))
    
    while "  " in name_school:
        name_school = name_school.replace("  ", " ")

    try:
        num = re.findall("\d+", name_school)[0]
    
    except:
        num = 0

    name_school = name_school.split()
    
    for word in name_school:
        for line in responce:
            if word in line["name"].lower():
                res.append(line["shortName"])
    
    school = None
    max_count = 0
    for el in res:
        if res.count(el) > max_count:
            if num != None:
                if str(num) in el:
                    max_count = res.count(el) + 3
                    school = el
            else:
                max_count = res.count(el)
                school = el
    return school