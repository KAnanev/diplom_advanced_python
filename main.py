import time
import json
import prompt

from scripts.class_user import User
from db.db_scripts import DB
from scripts.functions_collect import collect_list, collect_json_list
from pprint import pprint
from scripts.function_add_dir import add_dir


def main():
    login = prompt.string('Введите Ваш логин: ')
    password = prompt.secret('Введите Ваш Пароль: ')
    user = prompt.string('Введите Ваш ID: ')

    user_main = User(login, password)
    user_main.get_user(user)

    with DB() as connect:
        connect.create_db()
        if not connect.select_main_user(user_main.user_id):
            connect.insert_main_user(user_main.user_id)
        user_db_id = connect.select_main_user(user_main.user_id)[0][0]
        db_target_users = connect.select_target_users(user_db_id)

    list_target_users = collect_list(db_target_users, user_main.find_pair())

    with DB() as connect:
        connect.insert_target_users(user_db_id, list_target_users)

    def collect_temp_list_photo(user_id):
        temp_list_photo = []
        for i in user_main.get_target_user(user_id):
            temp_list_photo.append({
                'id': i['owner_id'],
                'comments': i['comments']['count'],
                'likes': i['likes']['count'],
                'photo': sorted(i['sizes'],
                                key=lambda x: x['height'])[-1]['url']
            })
        return temp_list_photo

    def collect_list_photo(list_user):
        count = 0
        list_photo = []
        for item in list_user:
            count += 1
            if count == 7:
                time.sleep(2)
                count = 0
            list_photo.append(
                sorted(collect_temp_list_photo(item),
                       key=lambda x: (
                           x['likes'], x['comments']), reverse=True
                       )[:3]
            )
        return list_photo

    output_list = collect_json_list(
        collect_list_photo(
            list_target_users)
    )
    pprint(output_list)

    add_dir()

    with open(
            'output_file/data_id{0}.json'.format(user_main.user_id),
            'w'
    ) as f:
        f.write(json.dumps(output_list))


if __name__ == '__main__':
    main()
