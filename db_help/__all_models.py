import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    vk=sqlalchemy.Column(sqlalchemy.Boolean,nullable=False)
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    nick = sqlalchemy.Column(sqlalchemy.String)
    menu = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
