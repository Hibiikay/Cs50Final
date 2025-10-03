# app.py
import os
import sqlite3
import random
import string
import io
from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
    flash,
    send_file,
)
from werkzeug.utils import secure_filename
from flask_session import Session
from fpdf import FPDF

# ---------- Config ----------
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "hunger.db")
UPLOAD_DIR = os.path.join(APP_DIR, "static", "receipts")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXT = {"png", "jpg", "jpeg", "pdf"}

# Admin credentials (change in production; or store in env vars)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "secret123"

# Flask app
app = Flask(__name__)
app.secret_key = "change_this_secret"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# ---------- DB helper ----------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- helpers ----------
def gen_player_id():
    return "HF-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

def apology(message):
    return render_template("apology.html", message=message)

# ---------- Routes ----------
@app.route("/")
def index():
    return render_template("index.html")

# Register user (player or supporter)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        play = request.form.get("play")

        if not name or not email or play not in ("yes", "no"):
            flash("All fields required.")
            return redirect(url_for("register"))

        conn = get_db()
        cur = conn.cursor()

        player_id = gen_player_id() if play == "yes" else None
        club = random.choice(["Lions FC", "Eagles FC", "Sharks FC", "Tigers FC"]) if play == "yes" else None

        try:
            cur.execute(
                "INSERT INTO users (name, email, play, player_id, club) VALUES (?, ?, ?, ?, ?)",
                (name, email, play, player_id, club),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            flash("Email already registered.")
            return redirect(url_for("register"))

        conn.close()
        flash("Registered successfully! If you selected 'Yes' to play, please upload your ₦15,000 receipt.")
        return redirect(url_for("login_user"))

    return render_template("register.html")

# Simple user login (by email) - sets session['user_id']
@app.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if not email:
            flash("Email required.")
            return redirect(url_for("login_user"))

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        if not user:
            flash("No account with that email.")
            return redirect(url_for("login_user"))

        session["user_id"] = user["id"]
        flash("Logged in.")
        # Send player to upload page if they chose to play
        if user["play"] == "yes":
            return redirect(url_for("upload_receipt"))
        else:
            return redirect(url_for("donate"))
    return render_template("login.html")

# Admin login (separate)
@app.route("/admin/login", methods=["GET", "POST"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            flash("Admin logged in.")
            return redirect(url_for("roster"))
        else:
            flash("Invalid admin credentials.")
            return redirect(url_for("login_admin"))
    return render_template("admin_login.html")

# Logout both user/admin
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("index"))

# Upload receipt for players (requires login)
@app.route("/upload_receipt", methods=["GET", "POST"])
def upload_receipt():
    if "user_id" not in session:
        flash("Please log in first.")
        return redirect(url_for("login_user"))

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    if not user:
        conn.close()
        flash("User not found.")
        return redirect(url_for("index"))

    if user["play"] != "yes":
        conn.close()
        return apology("Only players upload receipts here.")

    if request.method == "POST":
        if "receipt" not in request.files:
            conn.close()
            flash("No file part.")
            return redirect(url_for("upload_receipt"))
        file = request.files["receipt"]
        if file.filename == "":
            conn.close()
            flash("No file selected.")
            return redirect(url_for("upload_receipt"))
        if not allowed_file(file.filename):
            conn.close()
            flash("File type not allowed. Allowed: png,jpg,jpeg,pdf")
            return redirect(url_for("upload_receipt"))

        # save with unique name: userID_timestamp_filename
        filename = secure_filename(file.filename)
        unique = f"{user['id']}_{int(datetime.now().timestamp())}_{filename}"
        savepath = os.path.join(UPLOAD_DIR, unique)
        file.save(savepath)

        # update DB: store only filename
        conn.execute("UPDATE users SET receipt = ? WHERE id = ?", (unique, user["id"]))
        # also record mandatory ₦15,000 donation (cash)
        conn.execute("INSERT INTO donations (donor, type, amount) VALUES (?, ?, ?)", (user["name"], "cash", 15000.0))
        conn.commit()
        conn.close()

        flash("Receipt uploaded and ₦15,000 donation recorded. Thank you!")
        return redirect(url_for("index"))

    conn.close()
    return render_template("upload_receipt.html", user=user)

# Donation route for supporters (requires login)
@app.route("/donate", methods=["GET", "POST"])
def donate():
    if "user_id" not in session:
        flash("Please log in first.")
        return redirect(url_for("login_user"))

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    if not user:
        conn.close()
        flash("User not found.")
        return redirect(url_for("index"))

    if request.method == "POST":
        dtype = request.form.get("type")
        amount = request.form.get("amount", "")
        if dtype not in ("cash", "food"):
            conn.close()
            flash("Invalid donation type.")
            return redirect(url_for("donate"))

        if dtype == "cash":
            try:
                a = float(amount)
            except ValueError:
                conn.close()
                flash("Enter a valid cash amount.")
                return redirect(url_for("donate"))
            conn.execute("INSERT INTO donations (donor, type, amount) VALUES (?, ?, ?)", (user["name"], "cash", a))
        else:
            conn.execute("INSERT INTO donations (donor, type, amount) VALUES (?, ?, ?)", (user["name"], "food", 0))
        conn.commit()
        conn.close()
        flash("Donation recorded. Thank you!")
        return redirect(url_for("index"))

    conn.close()
    return render_template("donate.html", user=user)

# Admin-only roster (view players, receipts links)
@app.route("/roster")
def roster():
    if not session.get("admin"):
        flash("Admin login required.")
        return redirect(url_for("login_admin"))

    conn = get_db()
    players = conn.execute("SELECT * FROM users WHERE play='yes' ORDER BY club, name").fetchall()
    conn.close()
    return render_template("roster.html", players=players)

# Admin-only export CSV
@app.route("/export_csv")
def export_csv():
    if not session.get("admin"):
        flash("Admin login required.")
        return redirect(url_for("login_admin"))

    conn = get_db()
    players = conn.execute("SELECT name, email, player_id, club FROM users WHERE play='yes' ORDER BY club, name").fetchall()
    conn.close()

    # write CSV into memory
    si = io.StringIO()
    import csv as _csv
    writer = _csv.writer(si)
    writer.writerow(["Name", "Email", "Player ID", "Club"])
    for p in players:
        writer.writerow([p["name"], p["email"], p["player_id"], p["club"]])
    mem = io.BytesIO()
    mem.write(si.getvalue().encode("utf-8"))
    mem.seek(0)
    return send_file(mem, as_attachment=True, download_name="roster.csv", mimetype="text/csv")

# Admin-only export PDF
@app.route("/export_pdf")
def export_pdf():
    if not session.get("admin"):
        flash("Admin login required.")
        return redirect(url_for("login_admin"))

    conn = get_db()
    players = conn.execute("SELECT name, player_id, club FROM users WHERE play='yes' ORDER BY club, name").fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Football Match Rosters", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    for p in players:
        pdf.cell(0, 8, f"{p['player_id']}  -  {p['name']}  ({p['club']})", ln=True)

    out = pdf.output(dest="S").encode("latin-1")
    mem = io.BytesIO(out)
    mem.seek(0)
    return send_file(mem, as_attachment=True, download_name="roster.pdf", mimetype="application/pdf")

# Leaderboard (public)
@app.route("/leaderboard")
def leaderboard():
    conn = get_db()
    rows = conn.execute("SELECT donor, SUM(amount) as total FROM donations GROUP BY donor ORDER BY total DESC").fetchall()
    total = conn.execute("SELECT SUM(amount) FROM donations").fetchone()[0] or 0
    conn.close()
    return render_template("leaderboard.html", rows=rows, total=total)

# Serve uploaded files are in static/receipts so they are served by Flask automatically.
# Only admin links to them are shown in roster.html.

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
