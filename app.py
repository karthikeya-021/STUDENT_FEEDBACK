from flask import Flask, render_template, request, redirect
import mysql.connector
from config import db_config

app = Flask(__name__)

# Function to get a MySQL connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print("Database connection error:", err)
        return None

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Feedback page
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        comment = request.form.get('comment')

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                query = "INSERT INTO feedback (student_name, email, comment) VALUES (%s, %s, %s)"
                cursor.execute(query, (name, email, comment))
                conn.commit()
            except mysql.connector.Error as e:
                print("Error inserting data:", e)
            finally:
                cursor.close()
                conn.close()
        return redirect('/')
    
    return render_template('feedback.html')

# Admin page
@app.route('/admin')
def admin():
    conn = get_db_connection()
    feedbacks = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM feedback ORDER BY submitted_at DESC")
            feedbacks = cursor.fetchall()
        except mysql.connector.Error as e:
            print("Error fetching data:", e)
        finally:
            cursor.close()
            conn.close()
    return render_template('admin.html', feedbacks=feedbacks)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)