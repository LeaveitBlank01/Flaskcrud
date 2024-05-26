from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import os
from marshmallow import Schema, fields, ValidationError
import dicttoxml


app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '1234')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'new_schema')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

class PeopleSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    age = fields.Int(required=True)
    city = fields.Str()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/people", methods=["GET"])
def get_people():
    output_format = request.args.get('format', 'json')
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM people")
        data = cur.fetchall()
    return format_response(data, output_format)

@app.route("/people/<int:person_id>", methods=["GET"])
def get_person_by_id(person_id):
    output_format = request.args.get('format', 'json')
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM people WHERE id = %s", (person_id,))
        data = cur.fetchall()
    if not data:
        return jsonify({"error": "Person not found"}), 404
    return format_response(data[0], output_format)
@app.route("/people", methods=["POST"])
def create_person():
    try:
        data = PeopleSchema().load(request.get_json())
        first_name = data['first_name']
        last_name = data['last_name']
        age = data['age']
        city = data.get('city')

        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO people (first_name, last_name, age, city) VALUES (%s, %s, %s, %s)", (first_name, last_name, age, city))
            mysql.connection.commit()
            created_person_id = cur.lastrowid

        return jsonify({"message": "Person created successfully", "id": created_person_id}), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@app.route("/people/<int:person_id>", methods=["PUT"])
def update_person(person_id):
    output_format = request.args.get('format', 'json')
    try:
        data = PeopleSchema().load(request.get_json())
        first_name = data['first_name']
        last_name = data['last_name']
        age = data['age']
        city = data.get('city')

        with mysql.connection.cursor() as cur:
            cur.execute("UPDATE people SET first_name = %s, last_name = %s, age = %s, city = %s WHERE id = %s", (first_name, last_name, age, city, person_id))
            mysql.connection.commit()

        return format_response({"message": "Person updated successfully"}, output_format)
    except ValidationError as err:
        return format_response(err.messages, output_format)

@app.route("/people/<int:person_id>", methods=["DELETE"])
def delete_person(person_id):
    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM people WHERE id = %s", (person_id,))
        mysql.connection.commit()

    return jsonify({"message": "Person deleted successfully"}), 200

def format_response(data, output_format='json'):
    if output_format == 'xml':
        xml_data = dicttoxml.dicttoxml(data)
        return Response(xml_data, mimetype='text/xml')
    else:
        return jsonify(data)  # Default to JSON


if __name__ == "__main__":
    app.run(debug=True)
