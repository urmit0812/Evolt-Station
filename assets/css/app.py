from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('ev_charging_quotes.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for the quote form
@app.route('/', methods=['GET', 'POST'])
def get_quote():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        service = request.form['service']
        message = request.form['message']

        conn = get_db_connection()
        conn.execute('INSERT INTO quotes (name, email, phone, address, service, message) VALUES (?, ?, ?, ?, ?, ?)',
                     (name, email, phone, address, service, message))
        conn.commit()
        conn.close()
        return redirect(url_for('success'))

    return render_template('index.html')

# Route for the success page
@app.route('/success')
def success():
    return "Your quote request has been successfully submitted! We will get back to you shortly."

# Create the quotes table if it doesn't exist
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            service TEXT NOT NULL,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
