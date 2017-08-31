#1/usr/bin/python
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def get_engine():
    engine = create_engine("mysql://root:password@10.58.89.203/ansible_trainning?charset=utf8")
    return engine

def get_session(autocommit=True, expire_on_commit=False):
    Session = sessionmaker(bind=get_engine(),autocommit = autocommit, expire_on_commit = expire_on_commit)
    session = Session()
    return session

