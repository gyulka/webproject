from pprint import pprint
from flask import Flask, render_template, request, jsonify
from db_help import db_session
from db_help.__all_models import User

app = Flask(__name__)


def main():
    global session
    db_session.global_init("db/db.db")
    session = db_session.create_session()
    app.run()


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
        user.nick = request.args['nick']
        session.add(user)
        session.commit()
        return jsonify(succes=True)
    except Exception as error:
        return jsonify(succes=False, error=error.__str__())


@app.route('/api/set_nick')
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
        jsonify(succes=False, error=error.__str__())


@app.route('/api/get_all_users')  # не использовать, только для тестов
def get_all_users():
    for user in session.query(User):
        print(user.id)
    return jsonify(succes=True)


@app.route('/api/get_user')
def get_user():
    user = None
    try:
        user = [user for user in session.query(User).filter(User.id == int(request.args['id']), User.vk==(
            True if request.args['vk'] == 'True' else False))][0]
        return jsonify(succes=True, id=user.id, nick=user.nick, score=user.score, menu=user.menu)
    except IndexError as error:
        return jsonify(succes=False, error='no user was found')
    except Exception as error:
        return jsonify(succes=False, error=error.__str__())


@app.route('/api/set_menu')
def set_menu():
    try:
        id = int(request.args['id'])
        menu = int(request.args['menu'])
        for user in session.query(User).filter(User.id == int(request.args['id']), User.vk==(
                True if request.args['vk'] == 'True' else False)):
            user.menu = menu
        session.commit()
        return jsonify(succes=True)
    except Exception as error:
        jsonify(succes=False, error=error.__str__())


@app.route('/api/add_score')
def add_score():
    try:
        id = int(request.args['id'])
        score = int(request.args['score'])
        for user in session.query(User).filter(User.id == int(request.args['id']), User.vk==(
                True if request.args['vk'] == 'True' else False)):
            user.score += score
        session.commit()
        return jsonify(succes=True)
    except Exception as error:
        jsonify(succes=False, error=error.__str__())


if __name__ == '__main__':
    main()
