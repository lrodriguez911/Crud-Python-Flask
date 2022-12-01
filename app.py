from flask import Flask  # import framework
from flask import render_template, request, redirect
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()  # creating the object
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_PORT'] = 3307
app.config['MYSQL_DATABASE_BD'] = 'sistema_empleados'
mysql.init_app(app)


@app.route('/')
def index():
    sql = "INSERT INTO `sistema_empleados`.`employees` (`id`, `name`, `mail`, `photo`) VALUES (NULL, 'Lucas Rodriguez', 'lrodriguez.arevalosc@gmail.com', 'photo.png');"
    conn = mysql.connect()
    cursor = conn.cursor()
    #cursor.execute(sql)
    conn.commit()
    return render_template('employees/index.html')



@app.route('/create')
def create():
    return render_template('employees/create.html')


@app.route('/store', methods=['POST'])
def storage():
    name = request.form['txtName']
    mail = request.form['txtMail']
    photo = request.files['txtPhoto']
    sql = "INSERT INTO `sistema_empleados`.`employees` (`id`, `name`, `mail`, `photo`) VALUES (NULL, %s, %s, %s);"
    datos = (name, mail, photo.filename)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('employees/create.html')


if __name__ == '__main__':
    app.run(debug=True)
