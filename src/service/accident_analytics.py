from flask import Blueprint, jsonify, request
from src.manager.accident_analytics import AccidentAnalyticsManager
from flasgger import swag_from

ACCIDENT_ANALYTICS = Blueprint("accident_analytics", __name__)

@ACCIDENT_ANALYTICS.route("/accidents/hourly", methods=["GET"])
@swag_from("swag/get_hourly_accidents.yaml")
def get_hourly_accidents():
    try:
        manager = AccidentAnalyticsManager()
        result = manager.get_hourly_data()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ACCIDENT_ANALYTICS.route("/accidents/daily", methods=["GET"])
@swag_from("swag/get_daily_accidents.yaml")
def get_daily_accidents():
    try:
        manager = AccidentAnalyticsManager()
        result = manager.get_daily_data()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ACCIDENT_ANALYTICS.route("/accidents/monthly", methods=["GET"])
@swag_from("swag/get_monthly_accidents.yaml")
def get_monthly_accidents():
    try:
        manager = AccidentAnalyticsManager()
        result = manager.get_monthly_data()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ACCIDENT_ANALYTICS.route("/accidents/hotspots", methods=["GET"])
@swag_from("swag/get_hotspots.yaml")
def get_hotspots():
    try:
        manager = AccidentAnalyticsManager()
        result = manager.get_hotspots_data()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
