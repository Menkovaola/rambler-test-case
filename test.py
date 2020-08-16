import unittest

from sqlalchemy import create_engine

import schema
from repositories import GroupRepository
from schema import Group


class TestGroupRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.session = schema.init_db_session(engine=self.engine)

    def given_exists(self, obj):
        self.session.add(obj)
        self.session.commit()

    def test__should_save_group_data_when_not_exists(self):
        group_data: GroupRepository.GroupData = GroupRepository.GroupData(123, 'url', 'blabla')
        user_count_data: GroupRepository.AttributeData = GroupRepository.AttributeData('user_count', 199)

        repo: GroupRepository = GroupRepository(self.session)
        repo.save(group_data, user_count_data)

        group_obj: Group = self.session.query(Group).filter(Group.vk_id == group_data.group_id).first()
        self._checkGroupValidity(group_data, user_count_data, group_obj)

    def test__should_save_group_data_when_already_exists(self):
        self.given_exists(Group(123, 'name', 'url'))

        group_data: GroupRepository.GroupData = GroupRepository.GroupData(123, 'url', 'name')
        user_count_data: GroupRepository.AttributeData = GroupRepository.AttributeData('user_count', 199)

        repo: GroupRepository = GroupRepository(self.session)
        repo.save(group_data, user_count_data)

        group_obj: Group = self.session.query(Group).filter(Group.vk_id == group_data.group_id).first()
        self._checkGroupValidity(group_data, user_count_data, group_obj)

    def _checkGroupValidity(self, group_data: GroupRepository.GroupData, user_count_data: GroupRepository.AttributeData,
                            group_obj: Group):
        self.assertEqual(group_obj.url, group_data.group_url)
        self.assertEqual(group_obj.name, group_data.group_name)
        self.assertEqual(group_obj.vk_id, group_data.group_id)
        self.assertEqual(group_obj.group_attributes[0].name, user_count_data.attribute_name)
        self.assertEqual(group_obj.group_attributes[0].value, user_count_data.attribute_val)


if __name__ == '__main__':
    unittest.main()
