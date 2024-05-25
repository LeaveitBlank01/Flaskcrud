from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '1234')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'new_schema')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/people", methods=["GET"])
def get_people():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM people")
        data = cur.fetchall()
        cur.close()
        return jsonify(data)  
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

if __name__ == "__main__":
    app.run(debug=True)
