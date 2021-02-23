def collect_list(list_db, list_request):
    list_db = [i[2] for i in list_db]
    result = set(list_request).symmetric_difference(set(list_db))
    return list(result)[:10]


def collect_json_list(list_user):
    json_list = []
    for i in list_user:
        json_list.append(
            {'http://vk.com/id{0}'
                 .format(i[0]['id']): [j['photo'] for j in i]})
    return json_list
