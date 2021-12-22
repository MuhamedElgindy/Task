from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'DevOpsTask'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM courses order by date')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', courses = data)

@app.route('/add_course', methods=['POST'])
def add_course():
    if request.method == 'POST':
        name = request.form['course']
        price = request.form['price']
        date = request.form['date']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO courses (course_name, price, date) VALUES (%s,%s,%s)", (name, price, date))
        mysql.connection.commit()
        flash('Course Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_course(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM courses WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-course.html', course = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_course(id):
    if request.method == 'POST':
        course = request.form['course']
        price = request.form['price']
        date = request.form['date']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE courses
            SET course_name = %s,
                price = %s,
                date = %s
            WHERE id = %s
        """, (course, price, date, id))
        flash('Course Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_course(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM courses WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Course Removed Successfully')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=False)
