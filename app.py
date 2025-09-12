from flask import Flask, render_template
from datetime import datetime
from models import db, SystemLog, SharedFile
from utils import compress_file

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bosch.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def compress_file(input_path, output_path, level=3):
    cctx = zstd.ZstdCompressor(level=level)
    with open(input_path, "rb") as fin, open(output_path, "wb") as fout:
        fout.write(cctx.compress(fin.read()))


# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("home.html", datetime=datetime)


@app.route("/system_admin")
def system_admin():
    # Example logs – replace with db queries later
    logs = [
        {"id": 1, "message": "System started", "status": "OK", "timestamp": datetime.utcnow()},
        {"id": 2, "message": "Backup completed", "status": "OK", "timestamp": datetime.utcnow()},
        {"id": 3, "message": "Disk space low", "status": "Warning", "timestamp": datetime.utcnow()},
    ]

    # Example chart data
    chart_labels = ["OK", "Warning", "Error"]  # categories for chart
    chart_data = [2, 1, 0]  # counts matching above categories

    return render_template(
        "system_admin.html",
        logs=logs,
        chart_labels=chart_labels,
        chart_data=chart_data,
        datetime=datetime
    )


@app.route("/share_admin")
def share_admin():
    # Example files – replace with db queries later
    files = [
        {"id": 1, "filename": "report1.csv", "status": "Shared", "uploaded_at": datetime.utcnow()},
        {"id": 2, "filename": "data_backup.zip", "status": "Pending", "uploaded_at": datetime.utcnow()},
    ]

    # Prepare chart data
    chart_labels = [f["filename"] for f in files] if files else []
    chart_data = [1 for _ in files] if files else []  # Use 1 as a placeholder

    return render_template(
        "share_admin.html",
        files=files,
        chart_labels=chart_labels,
        chart_data=chart_data,
        datetime=datetime,
    )


@app.route("/user")
def user():
    return render_template("user.html", datetime=datetime)


# ---------- MAIN ----------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure DB tables exist
    app.run(debug=True)
