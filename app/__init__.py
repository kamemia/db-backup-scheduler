from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from app.tasks import backup_postgres_db_and_upload
from app.routes import routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes)

    # Start background backup job
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(backup_postgres_db_and_upload, 'interval', hours=24)
    scheduler.start()

    return app
