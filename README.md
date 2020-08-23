# mssql2json
Export users from Phoenix 4 to Casl Cloud
Для експорту відповідальних з об'єктів, завантажте програму https://github.com/dreikk91/mssql2json/releases/
Після першого запуску з'явиться export_phoenix_employee_config.yaml який потрібно відкрити в блокноті та замінити 127.0.0.1 на локальну ip адресу вашого сервера фенікс 4
Після повторного запуску, в папці з програмою з'явиться файл converted_sql.json, цей файл потрібно імпортувати в Casl Cloud

Пояснення про конфіг export_phoenix_employee_config.yaml

database: Pult4DB - назва бази даних

host: 127.0.0.1 - адрес сервера

object_number: '1' -  Наприклад у ваших об'єктів з приладами ajax пультовий починається з 'F' і ви хочите експортувати відповідальних тільки з аяксу, потрібно написати object_number: 'F', якщо хочете експортувати всіх відповідальних, напишіть object_number: ''

password: '' - Пароль від бази даних

username: sa - Ім'я Користувача

Всі дії ви робите на свій страх і ризик. Ніхто окрім вас не несе відповідальність за можливі збитки

To export those responsible for the objects, download the program https://github.com/dreikk91/mssql2json/releases/
After the first start, export_phoenix_employee_config.yaml will appear, which you need to open in Notepad and replace 127.0.0.1 with the local ip address of your Phoenix 4 server.
After restarting, the converted_sql.json file will appear in the program folder, this file must be imported into Casl Cloud

Explanation of config export_phoenix_employee_config.yaml

database: Pult4DB - the name of the database

host: 127.0.0.1 - server address

object_number: '1' - For example, for your objects with ajax devices, the object number starts with 'F' and you want to export only those responsible from ajax, you need to write object_number: 'F', if you want to export all those responsible, write object_number: ''

password: '' - Password from the database

username: sa - The name of the database user

All actions you take at your own risk. No one but you is responsible for any damages
