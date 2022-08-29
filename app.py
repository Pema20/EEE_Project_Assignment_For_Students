from flask import Flask, request, redirect, render_template
from models import db,Employee

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee_project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# binding the instance to a specific Flask application
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/')

def landing_page():  # put application's code here


    return 'You have landed EEE project-2022!'


@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':

        return render_template('createpage.html')


    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        gender = request.form['gender']
        position = request.form['position']
        age = request.form['age']
        phone = request.form['phone']
        email = request.form['email']
        employee = Employee(employee_id=employee_id, gender=gender, name=name, position=position, age=age, phone=phone,
                            email=email)
        db.session.add(employee)
        db.session.commit()
        return redirect('/data')


@app.route('/data')
def get_all_employees():
    employees = Employee.query.all()

    return render_template('datalist.html', employees=employees)


@app.route('/data/<int:id>')
def get_employee(id):
    employee = Employee.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee=employee)
    return f"Employee with id = {id} is not found in employee database"

@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    employee = Employee.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            name = request.form['name']
            gender = request.form['gender']
            position = request.form['position']
            age = request.form['age']
            phone = request.form['phone']
            email = request.form['email']
            employee = Employee(employee_id=id, gender=gender,name=name, position=position ,age=age ,phone=phone,email=email)
            db.session.add(employee)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Employee with id = {id} Does nit exist"

    return render_template('update.html', employee=employee)


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    employee = Employee.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()


            return redirect('/data')

    return render_template('delete.html')


if __name__ == '__main__':
    app.run(debug=True)

