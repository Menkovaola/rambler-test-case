from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vk_id: Column = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    created_date = Column(DateTime, default=func.current_timestamp(), nullable=False)

    def __init__(self, vk_id, name, url):
        self.vk_id = vk_id
        self.name = name
        self.url = url


class GroupAttribute(Base):
    __tablename__ = 'group_attributes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    created_date = Column(DateTime, default=func.current_timestamp(), nullable=False)
    value = Column(Integer, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship("Group", backref="group_attributes")
    __table_args__ = (Index('group_attributes_comp_group_name_date', "group_id", "name", "created_date"),)

    def __init__(self, name, value, group):
        self.name = name
        self.value = value
        self.group = group


def init_db_session(db_name):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine('sqlite:///' + db_name)

    Session = sessionmaker()
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)
    return Session()
