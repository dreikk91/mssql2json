import copy
import json
import logging
import time
from datetime import datetime

import pymssql
import yaml

logging.basicConfig(filename='export_phoenix_employee.log',
                    format='%(asctime)s-%(process)d-%(levelname)s-%(message)s', level=logging.DEBUG)
logging.info("Starting program")
logging.info("Try to open config")

try:
    with open('export_phoenix_employee_config.yaml') as f:
        yaml_config = yaml.safe_load(f)
        logging.info("Config opened successful")
except FileNotFoundError:
    logging.info("Can't open config, generating new")
    host = '127.0.0.1'
    object_number = ''
    username = 'sa'
    password = ''
    database = 'Pult4DB'
    to_yaml = { 'host': host,
                'username': username,
                'password': password,
                'database': database,
                'object_number': object_number}

    with open('export_phoenix_employee_config.yaml', 'w') as f:
        yaml.dump(to_yaml, f, default_flow_style=False)

    with open('export_phoenix_employee_config.yaml') as f:
        yaml_config = yaml.safe_load(f)

json_exemple = {
    "export_date": "2020-8-15",
    "type": "users",
    "data": [
        {
            "email": "",
            "last_name": "_",
            "first_name": "Денис",
            "middle_name": "_",
            "role": "IN_CHARGE",
            "images": [
                None
            ],
            "phone_numbers": [
                {
                    "active": True,
                    "number": "+38 (093) 111-11-11"
                }
            ]
        }
    ]
}

json_user = copy.deepcopy(json_exemple['data'][0])
json_exemple['export_date'] = datetime.now().strftime("%Y-%m-%d")

usercount = 0

print('Connecting to server %s' % yaml_config['host'])
host = yaml_config['host']
username = yaml_config['username']
password = yaml_config['password']
database = yaml_config['database']

conn = pymssql.connect(host, username, password, database)
cursor = conn.cursor()

cursor.execute("""
               SELECT u.ResponsiblesList_id, u.Responsible_Name, Responsible_Address, d.PhoneNo, c.panel_id, e.Description 
                FROM dbo.ResponsiblesList u
                INNER JOIN dbo.ResponsibleTel d ON u.ResponsiblesList_id = d.ResponsiblesList_id
                INNER JOIN dbo.Responsibles c ON d.ResponsiblesList_id = c.ResponsiblesList_id
                INNER JOIN dbo.ResponsibleTelDescription e ON d.ResponsibleTel_id = e.ResponsibleTel_id """)

rows = cursor.fetchmany(100000)


# print(list(set(rows)))


def remove_duplicates(listy):
    new_listy = []
    for i in listy:
        if i not in new_listy:
            new_listy.append(i)
    return new_listy


newrows = remove_duplicates(rows)
for row in newrows:
    # print(row)
    # print(row[4][0])

    if row[4][0] == yaml_config['object_number'] or yaml_config['object_number'] == '':

        username = row[1].split()
        obj_number = row[4]
        phone_number = row[3]
        try:
            json_user['last_name'] = copy.deepcopy(obj_number + ' ' + username[0])
        except IndexError as err:
            print(err)
            json_user['last_name'] = copy.deepcopy(obj_number)
        except KeyError as err:
            logging.info(err)
            json_user['last_name'] = copy.deepcopy(obj_number)
        try:
            json_user['first_name'] = copy.deepcopy(username[1])
        except IndexError as err:
            logging.info(err)
            json_user['first_name'] = copy.deepcopy(obj_number)
        except KeyError as err:
            logging.info(err)
            json_user['first_name'] = copy.deepcopy(obj_number)
        try:
            json_user['middle_name'] = copy.deepcopy(username[-1])
        except IndexError as err:
            logging.info(err)
            json_user['middle_name'] = copy.deepcopy(obj_number)
        except KeyError as err:
            logging.info(err)
            json_user['middle_name'] = copy.deepcopy(obj_number)

        try:
            if str(phone_number)[0] == '3':
                json_user['phone_numbers'][0]['number'] = '+' + str(phone_number)
            else:
                json_user['phone_numbers'][0]['number'] = '+38' + str(phone_number)
        except IndexError as err:
            logging.info(err)
            json_user['phone_numbers'][0]['number'] = ''

        json_exemple['data'].insert(copy.deepcopy(usercount), copy.deepcopy(json_user))
        usercount += 1

json_result = json.dumps(json_exemple, ensure_ascii=False, indent=4).encode('utf8').decode('utf8')
with open('converted_sql.json', 'w', encoding='utf8') as outfile:
    outfile.write(json_result)
print('Total exported employees %s' % usercount)
time.sleep(10)