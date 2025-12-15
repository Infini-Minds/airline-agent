from flask import Flask, Blueprint, request, jsonify
from api.reader import get_session_and_engine
from api.airline_service.threat_service import (
    process_city_bomb_threat,
    get_incident_feed,
    get_bookings,
    get_status_distribution,
    get_escalation_rate,
    get_dashboard_map_data
)

api = Blueprint("airline_api", __name__)

# -------------------
# DASHBOARD SUMMARY
# -------------------
@api.route("/dashboard/summary", methods=["GET"])
def dashboard_summary():
    session, _ = get_session_and_engine()
    try:
        return jsonify(get_incident_feed(session))
    finally:
        session.close()


# -------------------
# BOOKINGS & VOUCHERS
# -------------------
@api.route("/bookings", methods=["GET"])
def bookings():
    flight = request.args.get("flight")
    city = request.args.get("city")
    session, _ = get_session_and_engine()
    try:
        return jsonify(get_bookings(session, flight, city))
    finally:
        session.close()


# -------------------
# ANALYTICS
# -------------------
@api.route("/analytics/status-distribution", methods=["GET"])
def analytics_status():
    session, _ = get_session_and_engine()
    try:
        return jsonify(get_status_distribution(session))
    finally:
        session.close()


@api.route("/analytics/escalation-rate", methods=["GET"])
def analytics_escalation():
    session, _ = get_session_and_engine()
    try:
        return jsonify(get_escalation_rate(session))
    finally:
        session.close()


@api.route("/bomb-threat/city", methods=["POST"])
def bomb_threat_city():
    city = request.args.get("city")
    alt = request.args.get("alternate_airport")
    if not city:
        return jsonify({"error": "city required"}), 400
    session, _ = get_session_and_engine()
    try:
        with session.begin():
            return jsonify(process_city_bomb_threat(session, city, alt)), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@api.route("/dashboard/map", methods=["GET"])
def dashboard_map():
    print("inside map data")
    session, _ = get_session_and_engine()
    try:
        return jsonify(get_dashboard_map_data(session))
    finally:
        session.close()


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
