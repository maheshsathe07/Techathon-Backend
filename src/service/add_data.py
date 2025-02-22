from flask import Blueprint, jsonify, request
from flasgger.utils import swag_from
from src.manager.add_data import add_new_location

# Create Blueprint for the API
ADD_LOCATION_DATA = Blueprint("add_location_data", __name__)

@ADD_LOCATION_DATA.route("/add-location-data", methods=["POST"])
@swag_from("swag/add_data.yaml")
def add_location():
    """
    API endpoint to add new location data.
    """
    try:
        # Check Content-Type header
        if request.content_type != 'application/json':
            return jsonify({
                "error": "Content-Type must be application/json"
            }), 415

        # Get JSON data from request body
        data = request.get_json(silent=True)
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Extract parameters from JSON body
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # Debug logging
        print(f"Received data: {data}")

        # Validate required parameters
        if not all([latitude is not None, longitude is not None]):
            missing = [param for param in ["latitude", "longitude"] 
                      if data.get(param) is None]
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing)}"
            }), 400

        # Basic coordinate validation
        try:
            lat = float(latitude)
            lng = float(longitude)
            if not (-90 <= lat <= 90 and -180 <= lng <= 180):
                return jsonify({"error": "Invalid coordinates range"}), 400
        except ValueError:
            return jsonify({"error": "Coordinates must be numeric"}), 400

        # Add the new location
        location_id = add_new_location(latitude, longitude)

        # Return success response
        return jsonify({
            "message": "Location data added successfully",
            "location_id": str(location_id)
        }), 201

    except Exception as e:
        print(f"Error in add_location: {str(e)}")
        return jsonify({"error": str(e)}), 500