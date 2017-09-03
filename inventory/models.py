# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Group(Base):
    __tablename__ = 'groups'
    __table_args__ = {u'schema': 'ansible_trainning'}

    id = Column(Integer, primary_key=True)
    name = Column(String(255, u'utf8_bin'), unique=True, server_default=text("''"))
    username = Column(String(255, u'utf8_bin'))
    password = Column(String(255))
    host_list = relationship('Host', order_by='Host.id')


class Host(Base):
    __tablename__ = 'hosts'
    __table_args__ = {u'schema': 'ansible_trainning'}

    id = Column(Integer, primary_key=True)
    IP = Column(String(255, u'utf8_bin'))
    group_id = Column(ForeignKey(u'ansible_trainning.groups.id'), index=True)
    software = Column(String(255, u'utf8_bin'))
    group = relationship(u'Group')
