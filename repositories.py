from sqlalchemy import exists

from schema import Group, GroupAttribute


class GroupRepository:

    def __init__(self, db_session):
        self._db_session = db_session

    class GroupData:
        def __init__(self, group_id, group_url, group_name):
            self.group_id = group_id
            self.group_url = group_url
            self.group_name = group_name

    class AttributeData:
        def __init__(self, attribute_name, attribute_val):
            self.attribute_name = attribute_name
            self.attribute_val = attribute_val

    def save(self, group_data: GroupData, attribute_data: AttributeData):
        group_exists = self._db_session.query(exists().where(Group.vk_id == group_data.group_id)).scalar()
        if not group_exists:
            group = Group(vk_id=group_data.group_id, name=group_data.group_name, url=group_data.group_url)
            self._db_session.add(group)
        else:
            group = self._db_session.query(Group).filter(Group.vk_id == group_data.group_id).first()
        self._db_session.add(GroupAttribute(attribute_data.attribute_name, attribute_data.attribute_val, group))
        self._db_session.commit()
