import os
import unittest

from flask import url_for, abort
from flask_login import login_user, current_user
from flask_testing import TestCase
from app import db, create_app
from app.models import Employee, Department, Role


class TestBase(TestCase):
    BASE_DIR = os.path.dirname(__file__)

    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        app.config['WTF_CSRF_ENABLED'] = False

        # app.config.update(
        #     SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(TestBase.BASE_DIR, "dreamteam_test_db.sqlite3")
        # )

        return app

    def setUp(self):
        db.create_all()
        admin = Employee(username="admin", email="admin@email.org", password="admin2016", is_admin=True)
        employee = Employee(username="test_user",email="user@email.org", password="test2016")
        db.session.add_all([admin, employee])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestModels(TestBase):
    def test_employee_model(self):
        self.assertEqual(Employee.query.count(), 2)

    def test_department_model(self):
        department = Department(name='IT', description='The IT department')
        db.session.add(department)
        db.session.commit()
        self.assertEqual(Department.query.count(),1)

    def test_role_model(self):
        role = Role(name='TestRole',description='Test role')
        db.session.add(role)
        db.session.commit()
        self.assertEqual(Role.query.count(),1)

class TestViews(TestBase):

    def test_homepage_view(self):
        response = self.client.get(url_for('home.homepage'))
        # self.assertEqual(response.status_code,200)
        self.assert200(response)

    def test_login_view(self):
        response = self.client.get(url_for('auth.login'))
        # self.assertEqual(response.status_code,200)
        self.assert200(response)

    def login(self,email,passw):

        return self.client.post(url_for('auth.login'),data={'email':email,'password':passw},follow_redirects=False)


    def redirects_to_login(self, url):
        target_url = url_for(url)
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        # self.assertEqual(response.status_code, 302)
        self.assertStatus(response,302)
        self.assertRedirects(response,redirect_url)

    def test_logout_view(self):
        self.redirects_to_login('auth.logout')

    def test_dashboard_view(self):
        """test dashboard inaccessible without login"""
        self.redirects_to_login('home.dashboard')

    def test_admin_dashboard_view(self):
        """test admin dashboard inaccessible without login"""
        self.redirects_to_login('home.admin_dashboard')

    def test_departments_view(self):
        self.redirects_to_login('admin.list_departments')

    def test_roles_view(self):
        self.redirects_to_login('admin.list_roles')

    def test_employees_view(self):
        self.redirects_to_login('admin.list_employees')

    def test_user_login(self):
        resp = self.login('test@email.org', 'test2016')
        self.assert200(resp)

    def test_admin_login(self):
        resp = self.login('admin@email.org', 'admin201')
        print(resp.data)
        self.assert200(resp)

class TestErrorPages(TestBase):
    def test_403_forbidden(self):
        @self.app.route('/403')
        def forbidden_error():
            abort(403)
        resp = self.client.get('/403')

        self.assert403(resp)
        self.assertTrue(b'403 Error' in resp.data)

    def test_404_not_found(self):
        resp = self.client.get('/nothing')
        self.assert404(resp)
        self.assertTrue(b'404 Error' in resp.data)

    def test_500_internal_server_error(self):
        @self.app.route('/500')
        def internal_server_error():
            abort(500)
        resp = self.client.get('/500')

        self.assert500(resp)
        self.assertTrue(b'500 Error' in resp.data)


# if __name__ == '__main__':
#     unittest.main()
