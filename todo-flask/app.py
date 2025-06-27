from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import config

app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

# Show all tasks
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM todos")
    tasks = cur.fetchall()
    cur.close()
    return render_template('index.html', tasks=tasks)

# Add new task
@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

# Delete task
@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM todos WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

# Mark task as done/undone
@app.route('/toggle/<int:id>')
def toggle(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE todos SET done = NOT done WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
