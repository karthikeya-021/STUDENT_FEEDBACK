from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'feedback'


mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        comment = request.form['comment']
        cur = mysql.connection.cursor()
        try:
            cur.execute(
                "INSERT INTO feedback (student_name, email, comment) "
                "VALUES (%s, %s, %s)",
                (name, email, comment)
            )
            mysql.connection.commit()
        except Exception as e:
            print("Error inserting data:", e)
        finally:
            cur.close()
        return redirect('/')
    return render_template('feedback.html')

@app.route('/admin')
def admin():
    cur = mysql.connection.cursor()
    feedbacks = []
    try:
        cur.execute("SELECT * FROM feedback ORDER BY submitted_at DESC")
        feedbacks = cur.fetchall()
    except Exception as e:
        print("Error fetching data:", e)
    finally:
        cur.close()
    return render_template('admin.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(debug=True)
