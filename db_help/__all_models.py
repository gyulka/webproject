import config
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    vk = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    nick = sqlalchemy.Column(sqlalchemy.String)
    menu = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    count1 = sqlalchemy.Column(sqlalchemy.Integer)
    count2 = sqlalchemy.Column(sqlalchemy.Integer)
    count3 = sqlalchemy.Column(sqlalchemy.Integer)
    count4 = sqlalchemy.Column(sqlalchemy.Integer)
    count5 = sqlalchemy.Column(sqlalchemy.Integer)

    def update(self):
        self.score += self.count1 * config.perfomance1 + self.count2 * config.perfomance2 + self.count3 * config.perfomance3 + self.count4 * config.perfomance4 + self.count5 * config.perfomance5
