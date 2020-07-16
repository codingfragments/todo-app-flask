import nerdvision
import helper
from flask import Flask, request, Response
import json

app = Flask(__name__)

nerdvision.start(
    '0f559eee67892fb48c3e310e3cca4e06f4ab37cd007bf1013255926ceb26edb97c4e813cb05fd22f4f179dcc59786cecff416eec7d35f61095db7c5269ea813c',
    name="todoApp")


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/item/new', methods=['POST'])
def add_item():
    # Get item from the POST body
    req_data = request.get_json()
    item = req_data['item']

    # Add item to the list
    res_data = helper.add_to_list(item)

    # Return error if item not added
    if res_data is None:
        response = Response("{'error': 'Item not added - '}" +
                            item, status=400, mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response


@app.route('/items/all')
def get_all_items():
    # Get items from the helper
    res_data = helper.get_all_items()
    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response


@app.route('/item/status', methods=['GET'])
def get_item():
    # Get parameter from the URL
    item_name = request.args.get('name')

    # Get items from the helper
    status = helper.get_item(item_name)

    # Return 404 if item not found
    if status is None:
        response = Response("{'error': 'Item Not Found - '}" +
                            item_name, status=404, mimetype='application/json')
        return response

    # Return status
    res_data = {
        'status': status
    }

    response = Response(json.dumps(res_data), status=200,
                        mimetype='application/json')
    return response


@app.route('/item/update', methods=['PUT'])
def update_status():
    # Get item from the POST body
    req_data = request.get_json()
    item = req_data['item']
    status = req_data['status']

    # Update item in the list
    res_data = helper.update_status(item, status)
    if res_data is None:
        response = Response("{'error': 'Error updating item - '" + item +
                            ", " + status + "}", status=400, mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response


@app.route('/item/remove', methods=['DELETE'])
def delete_item():
    # Get item from the POST body
    req_data = request.get_json()
    item = req_data['item']

    # Delete item from the list
    res_data = helper.delete_item(item)
    if res_data is None:
        response = Response("{'error': 'Error deleting item - '" +
                            item + "}", status=400, mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response
