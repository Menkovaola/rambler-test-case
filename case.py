import vk  # Импортируем модуль vk

SERVICE_TOKEN = "75e08cd775e08cd775e08cd7967593f0fb775e075e08cd72ad8bf7cbd6c03be1dcf80d9"


def get_members(group_id):  # Функция формирования базы участников сообщества в виде списка
    # id = vk_api.utils.ResolveScreenName(screen_name=group)

    res = vk_api.groups.getMembers(group_id=group_id, v=5.122)  # Первое выполнение метода
    count = res["count"]  # Присваиваем переменной количество тысяч участников
    return count


def save_data(count, filename="data.txt"):  # Функция сохранения базы в txt файле
    with open(filename, "w") as file:  # Открываем файл на запись
        file.write("rambler/news" + "\t" + str(count) + "\n")


session = vk.Session(access_token=SERVICE_TOKEN)  # Авторизация
vk_api = vk.API(session)
rambler = get_members(group_id=97751087)
save_data(rambler)
