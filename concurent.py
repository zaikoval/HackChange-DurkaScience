import pandas as pd
import requests
import json
import numpy as np

#НИЖЕ РАССМАТРИВАЕТСЯ СЛУЧАЙ ДОБАВЛЕНИЯ В БАЗУ ДАННЫХ КОЛ-ВО БЛИЖАЙШИХ ПОЧТОВЫХ ОФИСОВ


PosKey = '0f777179-6c4a-4062-aa5d-a4540c667b10' #ключ для яндекс карт
OrgKey = '42012122-1af8-44d3-b2d0-b296e984a175' #ключ для яндекс организаций

table = pd.read_excel('olddata.xlsx', index_col=[0])   #чтение старой базы данных
streets = (table["ADDRESS"].tolist())   #добавление всех адресов в массив
nums = []

for i in streets:
    str = 'https://geocode-maps.yandex.ru/1.x/?apikey=0f777179-6c4a-4062-aa5d-a4540c667b10&geocode=' + i + '&format=json'
    #запрос для получения координат для определенного  адреса

    request = requests.get(str) #запрос на сервер Яндекса для получения координат
    jsn = json.loads(request.text)  #перевод в json

    c = jsn["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]   #получение координат из json
    #получение ближайших конкурентов для заданного магазина
    concurents = requests.get('https://search-maps.yandex.ru/v1/?text=Почта России&type=biz&lang=ru_RU&apikey='+OrgKey +
                              '&ll=' + c.split()[0] + ',' + c.split()[1] + '&spn=0.01,0.01&rspn=1&results=20')
    pickpoint = len(json.loads(concurents.text)['features'])  #узнает количество конкурентов
    nums.append(pickpoint)  #добавление в массив конкурентов

table['Почта России'] = pd.Series(np.random.randn(len(table)), index=table.index)#добавление в новую коллонку кол-во для каждого магазина

for i in range(len(table)):
    table.at[i, 'Почта России'] = nums[i]
table.to_excel('newdata.xlsx') #сохранение файла


