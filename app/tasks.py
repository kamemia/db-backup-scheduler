import os
from datetime import datetime
import subprocess
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))
bucket = os.getenv("SUPABASE_STORAGE_BUCKET")

def backup_postgres_db_and_upload():
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"supabase_backup_{now}.sql"
    backup_dir = os.path.join(os.getcwd(), "backups")
    os.makedirs(backup_dir, exist_ok=True)
    
    filepath = os.path.join(backup_dir, filename)
    env = os.environ.copy()
    env["PGPASSWORD"] = os.getenv("SUPABASE_DB_PASSWORD")
    try:
        result = subprocess.run(
            [
                "pg_dump",
                "-h", os.getenv("SUPABASE_DB_HOST"),
                "-U", os.getenv("SUPABASE_DB_USER"),
                "-d", os.getenv("SUPABASE_DB_NAME"),
                "-n", "public",
                "-F", "p",
                "-f", filepath,
            ],
            check=True,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        print(f"[+] Backup created at {filepath}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Backup failed: {e}")
        return

    try:
        with open(filepath, "rb") as f:
            supabase.storage.from_(bucket).upload(f"backups/{filename}", f)
        print(f"[+] Uploaded backup to Supabase: backups/{filename}")
    except Exception as e:
        print(f"[!] Upload failed: {e}")
