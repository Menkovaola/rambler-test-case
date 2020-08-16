import vk  # Импортируем модуль vk
import utils

def get_members(group):  # Функция формирования базы участников сообщества в виде списка
    # id = vk_api.utils.ResolveScreenName(screen_name=group)
    first = vk_api.groups.getMembers(group_id=97751087, v=5.122)  # Первое выполнение метода
    count = first["count"]  # Присваиваем переменной количество тысяч участников
    return count


def save_data(count, filename="data.txt"):  # Функция сохранения базы в txt файле
    with open(filename, "w") as file:  # Открываем файл на запись
         file.write("Рамблер/новости" + "\t" + str(count) + "\n")


if __name__ == "__main__":
    token = "75e08cd775e08cd775e08cd7967593f0fb775e075e08cd72ad8bf7cbd6c03be1dcf80d9"  # Сервисный ключ доступа
    session = vk.Session(access_token=token)  # Авторизация
    vk_api = vk.API(session)
    rambler = get_members("vk.com/rambler/")
    save_data(rambler)
