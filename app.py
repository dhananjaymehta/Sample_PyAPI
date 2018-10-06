#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import request
from flask import make_response

app = Flask(__name__)

# list of items
items = []


# -----------------
# Error Handling
# -----------------
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Check Input parameter'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'No Items in list'}), 404)


@app.errorhandler(408)
def not_found(error):
    return make_response(jsonify({'error': 'Out of range error'}), 408)


# -----------------
# POST Request
# -----------------
@app.route('/math/api/v1.0/', methods=['POST'])
def create_items_list():
    if not request.json or not 'items' in request.json:
        abort(400)
    else:
        items = sorted(request.json['items'])
        #return str(201)
        return jsonify({'items': items})


# -----------------
# GET Requests
# -----------------
# Min Request
@app.route('/math/api/v1.0/min/', methods=['GET'])
def get_min_items():
    if not request.json or not 'items' in request.json or not 'q' in request.json:
        abort(400)
    else:
        items = sorted(request.json['items'])
        quantifier = request.json['q']

        if not items:
            abort(404)

        if quantifier > len(items) or quantifier < 0 or not quantifier:
            abort(408)
        return jsonify({'min': items[:quantifier]})

# Max Request
@app.route('/math/api/v1.0/max/', methods=['GET'])
def get_max_items():
    if not request.json or not 'items' in request.json or not 'q' in request.json:
        abort(400)
    else:
        items = sorted(request.json['items'])
        quantifier = request.json['q']

        if not items:
            abort(404)

        if quantifier > len(items) or quantifier < 0 or not quantifier:
            abort(408)
        return jsonify({'max': items[-quantifier:]})

# Mean Request
@app.route('/math/api/v1.0/mean/', methods=['GET'])
def get_mean_of_items():
    if not request.json or not 'items' in request.json:
        abort(400)
    else:
        items = request.json['items']

        if not items:
            abort(404)

        return jsonify({'mean': round(sum(items) / len(items), 2)})

# Median Request
@app.route('/math/api/v1.0/median/', methods=['GET'])
def get_median_of_items():
    if not request.json or not 'items' in request.json:
        abort(400)
    else:
        items = sorted(request.json['items'])
        if not items:
            abort(404)

        mid = len(items) // 2
        if len(items) % 2 != 0:
            median = items[mid]
        else:
            median = (items[mid] + items[mid - 1]) / 2

        return jsonify({'median': round(median, 2)})

# Quartile

# -----------------
# MAIN
# -----------------
@app.route('/')
def index():
    return "Welcome to math api!!\nYou can perform from the following options: \n \n " \
           "1. Min \n 2. Max \n 3. Mean \n 4. Median \n 5. Percentile"

if __name__ == '__main__':
    app.run(debug=True)

# curl -i -H "Content-Type: application/json" -X POST -d '{"items":[3,2,1,7,5,4]}' http://localhost:5000/math/api/v1.0/
# curl -i -H "Content-Type: application/json" -X GET -d '{"items":[3,2,1,7,5,4], "q":2}' http://localhost:5000/math/api/v1.0/min/
# curl -i -H "Content-Type: application/json" -X GET -d '{"items":[3,2,1,7,5,4], "q":2}' http://localhost:5000/math/api/v1.0/max/
# curl -i -H "Content-Type: application/json" -X GET -d '{"items":[3,2,1,7,5,4]}' http://localhost:5000/math/api/v1.0/mean/
# curl -i -H "Content-Type: application/json" -X GET -d '{"items":[3,2,1,7,5,4]}' http://localhost:5000/math/api/v1.0/median/