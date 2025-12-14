from flask import Flask, Blueprint, request, jsonify
from api.airline_service.threat_service import process_city_bomb_threat

bomb_threat_api = Blueprint("bomb_threat_api", __name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bomb_threat_api)
    return app


@bomb_threat_api.route("/bomb-threat/city", methods=["POST"])
def bomb_threat_by_city():
    city = request.args.get("city")
    alternate_airport = request.args.get("alternate_airport")

    if not city:
        return jsonify({"error": "city is required"}), 400

    try:
        result = process_city_bomb_threat(city=city, alternate_airport=alternate_airport)
        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception as e:
        print(e)
        return jsonify({"error": "Bomb threat handling failed"}), 500

# --- Run App ---
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
