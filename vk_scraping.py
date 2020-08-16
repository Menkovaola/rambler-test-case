import datetime

import pandas as pd
import vk
from sqlalchemy import exists

import schema
from schema import Group, GroupAttribute


def get_members_count(_vk_api, group_id):
    res = _vk_api.groups.getMembers(group_id=group_id, v=5.122)
    count = res["count"]
    return count


def save_data(group_id, group_name, group_url, attr_name, attr_val, _db_session):
    group_exists = _db_session.query(exists().where(Group.vk_id == group_id)).scalar()
    if not group_exists:
        group = Group(vk_id=group_id, name=group_name, url=group_url)
        _db_session.add(group)
    else:
        group = _db_session.query(Group).filter(Group.vk_id == group_id).first()
    _db_session.add(GroupAttribute(attr_name, attr_val, group))
    _db_session.commit()


def scrape(service_token, file_name='input.csv', db_name='vk_analytics.sqlite'):
    print('Scraping vk groups attributes on {0}'.format(datetime.datetime.now()))
    db_session = schema.init_db_session(db_name)

    vk_api_session = vk.Session(access_token=service_token)  # Авторизация
    vk_api = vk.API(vk_api_session)

    urls = pd.read_csv(file_name)
    for group_url in urls['url']:
        try:
            group_name = group_url.split('/')[1]
            group_id = vk_api.groups.getById(group_id=group_name, v=5.122)[0]['id']
            save_data(group_id, group_name, group_url, 'user_count', get_members_count(vk_api, group_id=group_id),
                      db_session)
        except:
            print('Error occurred while processing for group url {0}'.format(group_url))
        finally:
            db_session.close()
