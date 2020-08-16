import datetime
from typing import List, Tuple

import pandas as pd
import vk

import schema
from repositories import GroupRepository


def _parse_urls(file_name) -> List:
    df = pd.read_csv(file_name)
    return df['url'].tolist()


def _vk_auth(service_token):
    vk_api_session = vk.Session(access_token=service_token)
    vk_api = vk.API(vk_api_session)
    return vk_api


def _get_user_count_attribute(_vk_api: vk.API, group_id) -> GroupRepository.AttributeData:
    res = _vk_api.groups.getMembers(group_id=group_id, v=5.122)
    return GroupRepository.AttributeData('user_count', res["count"])


def _get_group_info(_vk_api: vk.API, group_url, attribute_function) -> \
        Tuple[GroupRepository.GroupData, GroupRepository.AttributeData]:
    group_name = group_url.split('/')[1]
    group_id = _vk_api.groups.getById(group_id=group_name, v=5.122)[0]['id']
    return (GroupRepository.GroupData(group_id, group_url, group_name),
            attribute_function(_vk_api, group_id))


def _scrape(group_repository: GroupRepository, vk_api: vk.API, urls: List):
    for group_url in urls:
        try:
            (group_data, attribute_data) = _get_group_info(vk_api, group_url, _get_user_count_attribute)
            group_repository.save(group_data, attribute_data)
        except:
            print('Error occurred while processing for group url {0}'.format(group_url))


def scrape(service_token, file_name='input.csv', db_name='vk_analytics.sqlite'):
    print('Scraping vk groups attributes on {0}'.format(datetime.datetime.now()))
    urls = _parse_urls(file_name)
    vk_api = _vk_auth(service_token)
    db_session = schema.init_db_session(db_name)
    group_repository = GroupRepository(db_session)

    _scrape(group_repository, vk_api, urls)
    db_session.close()
