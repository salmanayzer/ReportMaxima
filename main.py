import requests
import ast
import csv
import random
import threading
from time import sleep
from datetime import datetime

list_id = []
list_time = []
token = ''

with open(r'report.csv', 'a', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=";", lineterminator="\r")
    filewriter.writerow(['date_time', 'value'])
    csvfile.close()


def report_new():
    while True:
        timestamp = datetime.today().timestamp()
        new_id = str(random.randint(1, 9999999999999))
        auth_token = token
        hed = {'Authorization': 'Bearer ' + auth_token}
        data = {'id': str(new_id)}

        url = 'https://analytics.maximum-auto.ru/vacancy-test/api/v0.1/reports'
        response = requests.post(url, json=data, headers=hed)
        data = str(data)
        dic = ast.literal_eval(data)
        if response.status_code == 201:
            print('Запрос на создание отчета принят. ')
            list_id.append(dic['id'])
            list_time.append(timestamp)
        elif response.status_code == 400:
            print('Тело запроса не соответствует спецификации. ')
        elif response.status_code == 404:
            print('Отчет с таким id уже существует ')
        else:
            print('Не верный токен ')
        sleep(60)


def report_receive():
    sleep(61)
    next_variable = 1
    identifiers = list_id[next_variable - 1]
    while True:
        auth_token = token
        hed = {'Authorization': 'Bearer ' + auth_token}

        url = 'https://analytics.maximum-auto.ru/vacancy-test/api/v0.1/reports/' + str(identifiers)
        response = requests.get(url, headers=hed)
        if response.status_code == 202:
            print('Отчет не готов')
        elif response.status_code == 400:
            print('Путь запроса не соответствует спецификации')
        elif response.status_code == 404:
            print('Отчет с таким id не существует.')
        elif response.status_code == 200:
            print('Отчет готов и записан в "csv" файл.')
            ccc = response.json()
            x = ccc['value']

            next_variable = next_variable + 1
            identifiers = list_id[next_variable - 1]

            auth_token = token
            hed = {'Authorization': 'Bearer ' + auth_token}

            url = 'https://analytics.maximum-auto.ru/vacancy-test/api/v0.1/reports/' + str(list_id[next_variable - 1])
            response = requests.get(url, headers=hed)
            with open(r'report.csv', 'a', newline='') as csvfile_report:
                filewriter_report = csv.writer(csvfile_report, delimiter=";", lineterminator="\r")
                filewriter_report.writerow([str(list_time[next_variable - 2]), str(x)])
                csvfile_report.close()

        sleep(60)


report_new = threading.Thread(target=report_new)
report_receive = threading.Thread(target=report_receive)

report_new.start()
report_receive.start()

report_new.join()
report_receive.join()
