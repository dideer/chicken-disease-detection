# run.py
from app import create_app
from app.models.user import User
from app.models.detection import Detection
# [VET-FEATURE] added VetReview import
from app.models.vet_review import VetReview

app = create_app()

# ← OUTSIDE if __name__ — runs on BOTH local and Render
try:
    User.create_table()
    Detection.create_table()
    # [VET-FEATURE] added VetReview table creation
    VetReview.create_table()
    User.ensure_default_admin()
    print("[INFO] All tables ready!")
except Exception as exc:
    print(f"[WARN] Skipping database initialization: {exc}")

if __name__ == '__main__':
    app.run(debug=False)
