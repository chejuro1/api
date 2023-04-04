from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('MONGODB_URI')
db = client['customer_db']
customers = db.customers

@app.route('/')
def home():
    return "Welcome to the customer service API!"

@app.route('/customers', methods=['GET'])
def get_customers():
    output = []
    for c in customers.find():
        output.append({'id': c['id'], 'name': c['name'], 'email': c['email']})
    return jsonify({'result': output})

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    c = customers.find_one({'id': id})
    if c:
        output = {'id': c['id'], 'name': c['name'], 'email': c['email']}
    else:
        output = {'error': 'Customer not found'}
    return jsonify({'result': output})

@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    customer = {'id': data['id'], 'name': data['name'], 'email': data['email']}
    result = customers.insert_one(customer)
    return jsonify({'id': str(result.inserted_id)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
