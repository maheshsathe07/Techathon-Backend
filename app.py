from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from src.service.add_data import ADD_LOCATION_DATA
from src.service.accident_analytics import *

app = Flask(__name__)
Swagger(app)  # Initialize Swagger

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow requests from all origins

# Register Blueprint
app.register_blueprint(ADD_LOCATION_DATA)
app.register_blueprint(ACCIDENT_ANALYTICS)


if __name__ == "__main__":
    app.run(debug=True, port=5000)