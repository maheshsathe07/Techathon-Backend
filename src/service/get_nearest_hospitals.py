from flask import Blueprint, request, jsonify
from src.manager.get_nearest_hospitals import get_nearest_hospitals
from flasgger import swag_from

GET_NEAREST_HOSPITALS = Blueprint('get_nearest_hospitals', __name__)

@GET_NEAREST_HOSPITALS.route('/find_nearest_hospitals', methods=['GET'])
@swag_from("swag/get_nearest_hospitals.yaml")
def find_nearest_hospitals():
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')

        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid latitude or longitude values"}), 400

    if latitude is None or longitude is None:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    # Get the nearest hospitals
    nearest_hospitals = get_nearest_hospitals(latitude, longitude)

    return jsonify({
        "message": "Nearest hospitals fetched successfully.",
        "nearest_hospitals": nearest_hospitals
    })
