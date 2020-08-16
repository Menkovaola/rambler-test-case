import vk  # Импортируем модуль vk
from sqlalchemy import exists

from schema import engine, Base, Group, GroupAttribute, Session, db_session

SERVICE_TOKEN = "75e08cd775e08cd775e08cd7967593f0fb775e075e08cd72ad8bf7cbd6c03be1dcf80d9"


def get_members(group_id):  # Функция формирования базы участников сообщества в виде списка
    # id = vk_api.utils.ResolveScreenName(screen_name=group)

    res = vk_api.groups.getMembers(group_id=group_id, v=5.122)  # Первое выполнение метода
    count = res["count"]  # Присваиваем переменной количество тысяч участников
    return count


def save_data(group_id, group_name, group_url, attr_name, attr_val, _db_session):
    group_exists = _db_session.query(exists().where(Group.vk_id == group_id)).scalar()
    if not group_exists:
        group = Group(vk_id=group_id, name=group_name, url=group_url)
        _db_session.add(group)
    else:
        group = _db_session.query(Group).filter(Group.vk_id == group_id).get()
    _db_session.add(GroupAttribute(attr_name, attr_val, group))
    _db_session.commit()


session = vk.Session(access_token=SERVICE_TOKEN)  # Авторизация
vk_api = vk.API(session)
vk_group_id = 97751087
count = get_members(group_id=vk_group_id)
save_data(vk_group_id, 'Rambler', 'some_url', 'count', count, db_session)
