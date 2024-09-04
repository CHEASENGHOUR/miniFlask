from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
from plyer import notification

app = Flask(__name__)
app.secret_key = "many random bytes"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud_db'
app.config['MYSQL_PORT'] = 3308

mysql = MySQL(app)


@app.route('/')
def Home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', users=data)


@app.route('/insert', methods=['POST'])
def Insert():
    if request.method == 'POST':
        # flash("Data inserted successfully")
        notification.notify(
            title="Data Inserted",
            message="Data inserted successfully",
            app_name="Hi Flask",
            timeout=15
        )
        Id = request.form['ID']
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (id, name, email) VALUES (%s, %s, %s)",
                    (Id, name, email))
        mysql.connection.commit()
        return redirect(url_for('Home'))


@app.route('/delete/<string:id_data>', methods=['GET'])
def Delete(id_data):
    notification.notify(
            title="Data Delete",
            message="Data Delete successfully",
            app_name="Hi Flask",
            timeout=15
        )
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Home'))


@app.route('/update', methods=['POST', 'GET'])
def Update():
    if request.method == 'POST':
        id_data = request.form['ID']
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET id=%s, name=%s, email=%s WHERE id = %s",
                    (id_data, name, email, id_data))
        mysql.connection.commit()
        notification.notify(
            title="Data Update",
            message="Data Update successfully",
            app_name="Hi Flask",
            timeout=15
        )
        return redirect(url_for('Home'))


if __name__ == '__main__':
    app.run(debug=True)
