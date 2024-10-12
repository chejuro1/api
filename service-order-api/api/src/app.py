from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import os

#########

# import logging
# from opencensus.ext.azure.log_exporter import AzureEventHandler

# logger = logging.getLogger(__name__)
# # Alternatively manually pass in the connection_string
# logger.addHandler(AzureEventHandler(connection_string="InstrumentationKey=eb85f8ac-b893-4766-8c85-4c99149f17d3"))
# logger.setLevel(logging.INFO)
# logger.info('Hello, World!')

########

app = Flask(__name__)
cors = CORS(app)
client = MongoClient(os.environ['MONGODB_URI'])
db = client[os.environ['MONGODB']]
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
