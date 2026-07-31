# run.py
from app import create_app
from app.models.user import User
from app.models.detection import Detection

app = create_app()

# ← OUTSIDE if __name__ — runs on BOTH local and Render
try:
    User.create_table()
    Detection.create_table()
    User.ensure_default_admin()
    print("[INFO] All tables ready!")
except Exception as exc:
    print(f"[WARN] Skipping database initialization: {exc}")

if __name__ == '__main__':
    app.run(debug=False)
