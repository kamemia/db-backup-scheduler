from flask import Blueprint, jsonify
from app.tasks import backup_postgres_db_and_upload
import traceback

routes = Blueprint("routes", __name__)

@routes.route("/backup-now", methods=["GET"])
def backup_now():
    try:
        backup_postgres_db_and_upload()
        return jsonify({"message": "Manual backup started successfully"}), 200
    except Exception as e:
        print("[!] Manual backup failed")
        traceback.print_exc()  # shows the full error in the terminal
        return jsonify({"error": str(e)}), 500
