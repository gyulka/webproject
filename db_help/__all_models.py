import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__='users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    nick = sqlalchemy.Column(sqlalchemy.String)
    menu = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
