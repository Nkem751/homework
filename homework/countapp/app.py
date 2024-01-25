# Import necessary libraries and modules
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
from decouple import config
import os
import re

# Create a Flask web application instance
app = Flask(__name__)

# Determine the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configure MySQL connection parameters using environment variables
app.config['MYSQL_HOST'] = config('DB_HOST')
app.config['MYSQL_PORT'] = int(config('DB_PORT'))
app.config['MYSQL_USER'] = config('DB_USER')
app.config['MYSQL_PASSWORD'] = config('DB_PASSWORD')
app.config['MYSQL_DB'] = config('DB_DATABASE')

# Create a MySQL instance for the Flask app
db = MySQL(app)

# Define a route for the home page ('/')
@app.route('/')
def home():
    # Create a cursor for interacting with the MySQL database
    cursor = db.connection.cursor(MySQLdb.cursors.Cursor)

    # Execute a SELECT query to fetch the current count from the 'counter' table
    cursor.execute("SELECT count FROM counter")
    
    # Fetch the result of the query (assuming 'counter' has a single row)
    cr = cursor.fetchone()

    # Calculate the incremented count
    inc = int(cr[0]) + 1

    # Execute an UPDATE query to increment the count in the 'counter' table
    cursor.execute("UPDATE counter set count = count + 1")

    # Commit the changes to the database
    cursor.connection.commit()

    # Close the cursor
    cursor.close()

    # Render the 'home.html' template with the incremented count
    return render_template('home.html', count=inc)

# Run the Flask application if this script is executed directly
if __name__ == "__main__":
    # Set the application to run on host '0.0.0.0' and port 6000 with debugging turned off
    app.run(debug=False, host='0.0.0.0', port=6000)
