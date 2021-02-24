import vk_requests
from scripts.functions_find_people import sex_pair
from scripts.functions_find_people import calculate_age

APP_ID = 7771470


class User:
    user_id = age = sex = city = relation = bdate = None

    def __init__(self, login, password):
        self.api = vk_requests.create_api(
            app_id=APP_ID,
            login=login,
            password=password,
            scope=['offline', 'photos', 'status'],
            interactive=True
        )

    def get_user(self, user):
        result = self.api.users.get(
            user_ids=user,
            fields='relation, sex, bdate, city'
        )[0]
        self.user_id = result['id']
        self.age = calculate_age(
            result['bdate'] if 'bdate' in result else input(
                'Введите Ваш возраст в формате dd.mm.yyyy: '
            )
        )
        self.relation = result['relation'] \
            if ('relation' in result) and (result['relation'] != 0) \
            else input('''Введите Ваш статус отношений, возможные значения:
1 — не женат (не замужем);
2 — встречается;
3 — помолвлен(-а);
4 — женат (замужем);
5 — всё сложно;
6 — в активном поиске;
7 — влюблен(-а);
8 — в гражданском браке: '''
                       )
        self.sex = result['sex'] if 'sex' in result \
            else input('Введите Ваш пол: ')

        def check_city(city):
            result_city = self.api.database.getCities(
                country_id=1,
                q=city
            )['items'][0]['id']
            return result_city

        self.city = result['city']['id'] if 'city' in result \
            else check_city(input('Введите Ваш город: '))

    def find_pair(self):

        temp_result = self.api.users.search(
            count=1000,
            user_ids=self.user_id,
            city=self.city,
            sex=sex_pair(self.sex),
            status=6,
            age_from=self.age - 5,
            age_to=self.age + 5
        )['items']

        result = []

        for i in temp_result:
            if i['can_access_closed']:
                result.append(i['id'])

        return result

    def get_target_user(self, target_id):
        result = self.api.execute(
            code='return [API.photos.get('
                 '{'
                 '"owner_id": ' + str(target_id) + ', '
                                                   '"album_id": "profile", '
                                                   '"rev": 1,'
                                                   '"extended": 1})]@.items;', v='5.92')
        return result[0]
