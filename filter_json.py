import copy
import json
import logging

import yaml

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
                'object_number': object_number,
                'from number': 1,
                'to number' : 9999,
                'slice start': 0,
                'slice end' : 4}

    with open('export_phoenix_employee_config.yaml', 'w') as f:
        yaml.dump(to_yaml, f, default_flow_style=False)

    with open('export_phoenix_employee_config.yaml') as f:
        yaml_config = yaml.safe_load(f)
try:
    with open('converted_sql.json', 'r', encoding='utf8') as f:
        json_dict = json.loads(f.read())
except FileNotFoundError as err:
    print(err)
new_dict = copy.deepcopy(json_dict)
new_dict['data'].clear()
for i in json_dict['data']:
    try:
        number = int(i['last_name'][yaml_config['slice start']:yaml_config['slice end']])
        # print(int(i['last_name'][0:4]))
        if number >= yaml_config['from number'] and number <= yaml_config['to number']:
            print(number)
            new_dict['data'].append(i)
    except ValueError as err:
        print(err)

json_result = json.dumps(new_dict, ensure_ascii=False, indent=4).encode('utf8').decode('utf8')
with open('converted_sql_filtered.json', 'w', encoding='utf8') as outfile:
    outfile.write(json_result)