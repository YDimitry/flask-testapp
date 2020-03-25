from flask import abort, redirect, render_template, url_for, flash
from flask_login import current_user, login_required

from ..models import Department, Role, Employee
from . import admin
from .. import db
from .forms import DepartmentForm, RoleForm, EmployeeAssignForm


def check_admin():
    if not current_user.is_admin:
        abort(403)


@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    check_admin()
    departments = Department.query.all()
    return render_template('admin/departments/departments.html', departments=departments)


@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    check_admin()
    add_department = True
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data, description=form.description.data)
        try:
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            flash('Error: department name already exists.')
        return redirect(url_for('admin.list_departments'))

    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")


@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    check_admin()
    add_department = False
    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')
        return redirect(url_for('admin.list_departments'))

    form.name.data = department.name
    form.description.data = department.description

    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def del_department(id):
    check_admin()
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')
    return redirect(url_for('admin.list_departments'))
    # return render_template(title="Delete Department")


@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    roles = Role.query.all()
    return render_template('admin/roles/roles.html', roles=roles)


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    check_admin()
    form = RoleForm()
    add_role = True
    if form.validate_on_submit():
        role = Role(name=form.name.data, description=form.description.data)
        try:
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added role')
        except:
            flash('Error: Role you trying to add already exists')
        return redirect(url_for('admin.list_roles'))
    return render_template('admin/roles/role.html', add_role=add_role, form=form)


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    check_admin()
    add_role = False
    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited role')
        return redirect(url_for('admin.list_roles'))
    form.name.data = role.name
    form.description.data = role.description

    return render_template('admin/roles/role.html', add_role=add_role, form=form)


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def del_role(id):
    check_admin()
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully removed role')

    return redirect(url_for('admin.list_roles'))


@admin.route('/employees')
@login_required
def list_employees():
    check_admin()
    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',employees=employees)


@admin.route('/employees/assign/<int:id>',methods=['GET','POST'])
@login_required
def assign_employee(id):
    check_admin()
    employee = Employee.query.get_or_404(id)
    if employee.is_admin:
        abort(403)
    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',employee=employee,form=form,title='Assign Employee')
