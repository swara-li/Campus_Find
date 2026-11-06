
from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)

DATABASE = Path(__file__).with_name("campus_find.db")


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            report_type TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            location TEXT NOT NULL,
            contact TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/api/reports", methods=["GET"])
def get_reports():
    search = request.args.get("q", "").strip()
    report_type = request.args.get("type", "").strip()

    connection = get_db_connection()

    query = "SELECT * FROM reports WHERE status = 'Open'"
    values = []

    if search:
        query += """
            AND (
                item_name LIKE ?
                OR location LIKE ?
                OR category LIKE ?
            )
        """
        term = f"%{search}%"
        values.extend([term, term, term])

    if report_type in ("Lost", "Found"):
        query += " AND report_type = ?"
        values.append(report_type)

    query += " ORDER BY created_at DESC"

    reports = connection.execute(query, values).fetchall()
    connection.close()

    return jsonify([dict(report) for report in reports])


@app.route("/api/reports", methods=["POST"])
def add_report():
    data = request.get_json(silent=True) or {}

    required_fields = [
        "item_name",
        "report_type",
        "category",
        "location",
        "contact"
    ]

    for field in required_fields:
        if not str(data.get(field, "")).strip():
            return jsonify({"error": f"{field} is required"}), 400

    if data["report_type"] not in ("Lost", "Found"):
        return jsonify({"error": "Choose Lost or Found"}), 400

    connection = get_db_connection()

    cursor = connection.execute("""
        INSERT INTO reports
        (item_name, report_type, category, description, location, contact)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["item_name"].strip(),
        data["report_type"],
        data["category"].strip(),
        data.get("description", "").strip(),
        data["location"].strip(),
        data["contact"].strip()
    ))

    connection.commit()
    report_id = cursor.lastrowid
    connection.close()

    return jsonify({
        "message": "Report added successfully",
        "id": report_id
    }), 201


@app.route("/api/reports/<int:report_id>/resolve", methods=["PATCH"])
def resolve_report(report_id):
    connection = get_db_connection()

    cursor = connection.execute("""
        UPDATE reports
        SET status = 'Resolved'
        WHERE id = ? AND status = 'Open'
    """, (report_id,))

    connection.commit()
    updated = cursor.rowcount
    connection.close()

    if updated == 0:
        return jsonify({"error": "Report not found or already resolved"}), 404

    return jsonify({"message": "Report marked as resolved"})


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
