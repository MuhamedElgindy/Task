from flask import Flask
import psycopg2
from psycopg2 import sql, extensions

# initializations
app = Flask(__name__)

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="1234",
    port = "5432")

table_name = "courses"
# create_table = "drop TABLE {}"
# cur = conn.cursor()
# cur.execute(sql.SQL(create_table).format(sql.Identifier( table_name )))
# conn.commit()


# Concatenate SQL string
create_table = "CREATE TABLE {} (id SERIAL PRIMARY KEY , course_name VARCHAR(128), price float(4), date DATE );"
cur = conn.cursor()

cur.execute(sql.SQL(create_table).format(sql.Identifier( table_name )))
conn.commit()


# # settings
# # app.secret_key = "mysecretkey"

cur = conn.cursor()
cur.execute("select * from courses")
row = cur.fetchall()

print(row)
cur.close()


# initializations
app = Flask(__name__)


# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = conn.cursor()
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
        cur = conn.cursor()
        cur.execute("INSERT INTO courses (course_name, price, date) VALUES (%s,%s,%s)", (name, price, date))
        conn.commit()
        flash('Course Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_course(id):
    cur = conn.cursor()
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
        cur = conn.cursor()
        cur.execute("""
            UPDATE courses
            SET course_name = %s,
                price = %s,
                date = %s
            WHERE id = %s
        """, (course, price, date, id))
        flash('Course Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_course(id):
    cur = conn.cursor()
    cur.execute('DELETE FROM courses WHERE id = {0}'.format(id))
    conn.commit()
    flash('Course Removed Successfully')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=5000)


