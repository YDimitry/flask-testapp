import pytest


from app import create_app, db
from app.models import Employee


@pytest.fixture()
def setup():
    flask_app = create_app('test')
    ctx = flask_app.app_context()
    ctx.push()

    db.create_all()

    user = Employee(email='qwer@asdf.ru',
                        username='qwer',
                        first_name='Qwerty',
                        last_name='Trewq',
                        password='asdf')
    db.session.add(user)
    db.session.commit()

    yield flask_app
    ctx.pop()


def test_new_user(setup):
    user = Employee.query.filter_by(username='qwer').first()
    assert user, "Пользователь не создан"
    assert user.verify_password('asdf'), "Пароль не прошел проверку"



if __name__ == "__main__":
    # pytest.main(['-v', '--tb', 'line'])
    pytest.main(['-v'])