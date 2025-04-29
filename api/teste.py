from flask import Flask, jsonify, request, make_response, abort
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)


#Mysql database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="api"
)

#create a connection for the database:
cursor = mysql-connector.connect(**mydb)

#route to teste the API
@app.route('/api/teste', methods=['GET'])
def test_api():
    return jsonify({'message': 'API IS WORKING BIIIITCH'})


# Route to create a new teacher
@app.route('/api/teachers', methods=['POST'])
def create_teacher():
    # Get the teacher data from the request
    teacher_data = request.get_json()
    # Insert the teacher data into the database
    cursor = cnx.cursor()
    query = "INSERT INTO teachers (name, email) VALUES (%s, %s)"
    cursor.execute(query, (teacher_data['name'], teacher_data['email']))
    cnx.commit()
    return jsonify({'message': 'Teacher created successfully!'})

#route to create a new rental
@app.route('/api/rentals', methods=['POST'])
def rent_a_classroom():
    rental_data = request.get_json()
    cursor = cnx.cursor()
    query = "INSERT INTO rentals (teacher_id, classroom_id, start_date, end_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (rental_data['teacher_id'], rental_data['classroom_id'], rental_data['start_date'], rental_data['end_date']))
    cnx.commit()
    return jsonify({'message': 'Rental created successfully!'})

if __name__ == '__main__':
    app.run(debug=True)

