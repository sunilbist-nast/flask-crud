from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE)''')
        
init_db()

@app.route('/')
def index():
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        students = cur.fetchall()
        return render_template('index.html', students=students)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        with sqlite3.connect("database.db") as conn:
            conn.execute("INSERT INTO students (name, email) VALUES (?, ?)", (name, email))
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            cur.execute("UPDATE students SET name=?, email=? WHERE id=?", (name, email, id))
            conn.commit()
            return redirect(url_for('index'))
        cur.execute("SELECT * FROM students WHERE id=?", (id,))
        student = cur.fetchone()
        return render_template('update.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    with sqlite3.connect("database.db") as conn:
        conn.execute("DELETE FROM students WHERE id=?", (id,))
        return redirect(url_for('index'))

if __name__ == '__main__':
 app.run(debug=True)
