import csv
from flask import Blueprint, request, jsonify,send_file
from app.services.purchase_services import fetch_purchase_data_from_csv, get_purchase_data,update_purchase_detail_data,delete_purchase_detail_data,create_purchase_csv
import os

purchase_bp = Blueprint('purchase', __name__)

@purchase_bp.route('/fatch_csv', methods=['POST'])
def fatch_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"})
    
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "Only CSV files are allowed"})

    try:
        fetch_purchase_data_from_csv(file)
        return jsonify({"message": "Data successfully processed and inserted into the database."})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 500

@purchase_bp.route('/get_purchase', methods=['GET'])
def get_purchase():
    bill_no = request.args.get('bill_no')
    if not bill_no:
        return jsonify({"error": "bill_no parameter is required"})

    result = get_purchase_data(bill_no)
    if result is None:
        return jsonify({"message": "No purchase found for the given bill number"})

    return jsonify(result), 200


@purchase_bp.route('/update_purchase_mrp',methods=['PUT'])
def update_purchase_mrp():
    data=request.get_json()
    result = update_purchase_detail_data(data)
    return jsonify(result)


@purchase_bp.route('/delete_purchase_data',methods=['DELETE'])
def delete_purchase_data():
    data=request.get_json()
    result = delete_purchase_detail_data(data)
    return jsonify(result)


@purchase_bp.route('/create_purchase_csv', methods=['GET'])
def create_csv_endpoint():
    result = create_purchase_csv()
    if result['status'] == 'success':
        return jsonify(result), 200
    else:
        return jsonify(result), 500