from flask import Flask  # import framework
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os


app = Flask(__name__)
mysql = MySQL()  # creating the object
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_PORT'] = 3307
app.config['MYSQL_DATABASE_BD'] = 'sistema_empleados'
mysql.init_app(app)


FOLDER = os.path.join('uploads')
app.config['FOLDER'] = FOLDER
print(FOLDER)

@app.route('/')
def index():
    sql = f"SELECT * FROM sistema_empleados.employees;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    employees = cursor.fetchall()
    #print(employees)
    conn.commit()
    return render_template('employees/index.html', employees=employees)


@app.route('/create')
def create():
    return render_template('employees/create.html')


@app.route('/store', methods=['POST'])
def storage():
    _name = request.form['txtName']
    _mail = request.form['txtMail']
    _photo = request.files['txtPhoto']

    now = datetime.now()  # time and date of upload
    time = now.strftime("%Y%H%M%S")

    if _photo.filename != '':
        newNamePhoto = time + _photo.filename
        _photo.save("uploads/" + newNamePhoto)

    sql = f"INSERT INTO `sistema_empleados`.`employees` (`id`, `name`, `mail`, `photo`) VALUES (NULL, '{_name}', '{_mail}', '{newNamePhoto}');"
    #datos = (_name, _mail, newNamePhoto)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return redirect('/')


@app.route('/destroy/<int:id>')
def destroy(id):
    sql = f"DELETE FROM sistema_empleados.employees WHERE id='{id}';"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT photo FROM sistema_empleados.employees WHERE id='{id}';")
    row = cursor.fetchall()
    os.remove(os.path.join(app.config['FOLDER'], row[0][0]))

    cursor.execute(sql, id)
    conn.commit()
    return redirect("/")


@app.route('/edit/<int:id>')
def edit(id):
    sql = f"SELECT * FROM `sistema_empleados`.`employees` WHERE id='{id}'"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    employees = cursor.fetchone()
    conn.commit()
    return render_template('employees/edit.html', employees=employees)


@app.route('/update', methods=['POST'])
def update():
    _name = request.form['txtName']
    _mail = request.form['txtMail']
    _photo = request.files['txtPhoto']
    id = request.form['txtId']

    sql = f"UPDATE sistema_employees.employees SET name='{_name}', mail='{_mail}' WHERE id='{id}';"
    
    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()  # time and date of upload
    time = now.strftime("%Y%H%M%S")

    if _photo.filename != '':
        newNamePhoto = time + _photo.filename
        _photo.save("uploads/"+newNamePhoto)

        cursor.execute(f"SELECT photo FROM sistema_empleados.employees WHERE id='{id}';")
        row = cursor.fetchall()
        os.remove(os.path.join(app.config['FOLDER'], row[0][0]))

        cursor.execute(f"UPDATE sistema_empleados.employees SET photo='{newNamePhoto}' WHERE id='{id}';")
        conn.commit()
        
    cursor.execute(sql)
    conn.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
