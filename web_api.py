from threading import Thread

import requests
import schedule
from flask import Flask, jsonify, request

import config
from db_help import db_session
from db_help.__all_models import User

app = Flask(__name__)


def updater():
    schedule.every().hours.at(':00').do(requests.get, config.db_server_api + 'update')
    while True:
        schedule.run_pending()


def main():
    global session
    db_session.global_init("db/db.db")
    session = db_session.create_session()
    th = Thread(target=updater)
    th.start()
    app.run(port=80)


@app.route('/api/add_user', methods=['POST'])
def add_user():
    try:
        if [user for user in session.query(User).filter(User.id == int(request.args['id']), User.vk == (
                True if request.args['vk'] == 'True' else False))]:
            return jsonify(succes=False, error='user is already exists')
        user = User()
        user.id = int(request.args['id'])
        user.vk = False if request.args['vk'] == 'False' else True
        user.score = 1000
        user.menu = 0
        user.count1 = 0
        user.count2 = 0
        user.count3 = 0
        user.count4 = 0
        user.count5 = 0
        user.nick = request.args['nick']
        user.helping = None
        session.add(user)
        session.commit()
        return jsonify(succes=True)
    except Exception as error:
        app.log_exception(error.__str__())
        return jsonify(succes=False, error=error.__str__())


@app.route('/api/set_nick', methods=['POST'])
def set_nick():
    try:
        id = int(request.args['id'])
        nick = request.args['nick']
        for user in session.query(User).filter(User.id == int(request.args['id']), User.vk == (
                True if request.args['vk'] == 'True' else False)):
            user.nick = nick
        session.commit()
        return jsonify(succes=True)
    except Exception as error:
        app.log_exception(error.__str__())
        jsonify(succes=False, error=error.__str__())


@app.route('/api/buy_1', methods=['POST'])
def buy_1():
    try:
        user = [user for user in session.query(User).filter(User.id == int(request.args['id']), User.vk == (
            True if request.args['vk'] == 'True' else False))][0]
        if user.score >= config.price1 * (1.1 ** user.count1):
            user.score -= config.price1 * (1.1 ** user.count1)
            user.count1 += 1
            session.commit()
            return jsonify(succes=True)
        else:
            return jsonify(succes=False, error='not enough money')
    except Exception as error:
        app.log_exception(error.__str__())
        return jsonify(succes=False, error=error.__str__())


@app.route('/api/buy_2', methods=['POST'])
def buy_2():
    try:
        user = [user for user in session.query(User).filter(User.id == int(request.args['id']), User.vk == (
            True if request.args['vk'] == 'True' else False))][0]
        if user.score >= config.price1 * (1.1 ** user.count2):
            user.score -= config.price1 * (1.1 ** user.count2)
            user.count2 += 1
            session.commit()
            return jsonify(succes=True)
        else:
            return jsonify(succes=False, error='not enough money')
    except Exception as error:
        app.log_exception(error.__str__())
        return jsonify(succes=False, error=error.__str__())


@app.route('/api/buy_3', methods=['POST'])
def buy_3():
    try:
        user = [user for user in session.query(User).filter(User.id == int(request.args['id']), User.vk == (
            True if request.args['vk'] == 'True' else False))][0]
        if user.score >= config.price1 * (1.1 ** user.count3):
            user.score -= config.price1 * (1.1 ** user.count3)
            user.count3 += 1
            session.commit()
            return jsonify(succes=True)
        else:
            return jsonify(succes=False, error='not enough money')
    except Exception as error:
        app.log_exception(error.__str__())
        return jsonify(succes=False, error=error.__str__())


@app.route('/api/buy_4', methods=['POST'])
def buy_4():
    try:
        user = [user for user in session.query(User).filter(User.id == int(request.args['id']), User.vk == (
            True if request.args['vk'] == 'True' else False))][0]
        if user.score >= config.price1 * (1.1 ** user.count4):
            user.score -= config.price1 * (1.1 ** user.count4)
            user.count4 += 1
            session.commit()
            return jsonify(succes=True)
        else:
            return jsonify(succes=False, error='not enough money')
    except Exception as error:
        app.log_exception(error.__str__())
        return jsonify(succes=False, error=error.__str__())


@app.route('/api/buy_5', methods=['POST'])
def buy_5():
    try:
        user = [user for user in session.query(User).filter(User.id == int(request.args['id']), User.vk == (
            True if request.args['vk'] == 'True' else False))][0]
        if user.score >= config.price1 * (1.1 ** user.count5):
            user.score -= config.price1 * (1.1 ** user.count5)
            user.count5 += 1
            session.commit()
            return jsonify(succes=True)
        else:
            return jsonify(succes=False, error='not enough money')
    except Exception as error:
        app.log_exception(error.__str__())
        return jsonify(succes=False, error=error.__str__())


@app.route('/api/get_all_users')  # не использовать, только для тестов
def get_all_users():
    for user in session.query(User):
        print(user.id)
    return jsonify(succes=True)


@app.route('/api/get_user', methods=['GET'])
def get_user():
    user = None
    try:
        user = [user for user in session.query(User).filter(User.id == int(request.args['id']), User.vk == (
            True if request.args['vk'] == 'True' else False))][0]
        return jsonify(succes=True, id=user.id, nick=user.nick, score=user.score, menu=user.menu, count1=user.count1,
                       count2=user.count2, count3=user.count3, count4=user.count4, count5=user.count5,
                       helping=user.helping)
    except IndexError as error:
        return jsonify(succes=False, error='no user was found')
    except Exception as error:
        app.log_exception(error.__str__())
        return jsonify(succes=False, error=error.__str__())


@app.route('/api/set_menu', methods=['POST'])
def set_menu():
    try:
        id = int(request.args['id'])
        menu = int(request.args['menu'])
        for user in session.query(User).filter(User.id == int(request.args['id']), User.vk == (
                True if request.args['vk'] == 'True' else False)):
            user.menu = menu
        session.commit()
        return jsonify(succes=True)
    except Exception as error:
        app.log_exception(error.__str__())
        jsonify(succes=False, error=error.__str__())


@app.route('/api/add_score', methods=['POST'])
def add_score():
    try:
        id = int(request.args['id'])
        score = int(request.args['score'])
        for user in session.query(User).filter(User.id == int(request.args['id']), User.vk == (
                True if request.args['vk'] == 'True' else False)):
            if user.score + score >= 0:
                user.score += score
        session.commit()
        return jsonify(succes=True)
    except Exception as error:
        app.log_exception(error.__str__())
        jsonify(succes=False, error=error.__str__())


@app.route('/api/update')
def update():
    try:
        for user in session.query(User):
            user.update()
        session.commit()
        return jsonify(succes=True)
    except Exception as error:
        app.log_exception(error.__str__())
        return jsonify(succes=False, error=error.__str__())


@app.route('/api/transfer', methods=['POST'])
def transfer():
    try:
        summ = int(request.args['score'])
        id_to = request.args['id_to']
        id_to, vk = id_to.split('_')
        id_from = int(request.args['id'])
        vk_from = True if request.args['vk'] == 'True' else False
        vk = bool(int(vk))
        id_to = int(id_to)
        user_from = [user for user in session.query(User).filter(User.id == id_from, User.vk == vk_from)][0]
        if user_from.score >= summ:
            user_to = [user for user in session.query(User).filter(User.id == id_to, User.vk == vk)][0]
            user_from.score -= summ
            user_to.score += summ
            session.commit()
            return jsonify(succes=True, nick_to=user_to.nick)
        else:
            return jsonify(succes=False, error='not enough money')
    except Exception as error:
        app.log_exception(error.__str__())
        return jsonify(succes=False, error=error.__str__())


@app.route('/api/set_helping', methods=['POST'])
def set_helping():
    try:
        user = [user for user in session.query(User).filter(User.id == int(request.args['id']), User.vk == (
            True if request.args['vk'] == 'True' else False))][0]
        user.helping = request.args['helping']
        session.commit()
        return jsonify(succes=True)
    except Exception as error:
        app.log_exception(error.__str__())
        return jsonify(succes=False, error=error.__str__())


@app.route('/')
def index():
    return '<h1>Привет!</h1>'


if __name__ == '__main__':
    main()
