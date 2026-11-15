
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "ucapan_tamu.db"


def buat_database():
    with sqlite3.connect(DB_NAME) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS ucapan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                kehadiran TEXT NOT NULL,
                jumlah_tamu INTEGER NOT NULL,
                ucapan TEXT NOT NULL,
                tanggal TEXT NOT NULL
            )
        """)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/kirim-ucapan", methods=["POST"])
def kirim_ucapan():
    data = request.get_json(silent=True) or request.form

    nama = str(data.get("nama", "")).strip()
    kehadiran = str(data.get("kehadiran", "")).strip()
    ucapan = str(data.get("ucapan", "")).strip()

    try:
        jumlah = int(data.get("jumlah_tamu", 1))
    except (ValueError, TypeError):
        return jsonify(status="error", pesan="Jumlah tamu tidak valid."), 400

    if not nama or not ucapan or kehadiran not in ["Hadir", "Tidak Hadir"]:
        return jsonify(status="error", pesan="Lengkapi data dengan benar."), 400

    if not 1 <= jumlah <= 10:
        return jsonify(status="error", pesan="Jumlah tamu maksimal 10."), 400

    with sqlite3.connect(DB_NAME) as db:
        db.execute("""
            INSERT INTO ucapan
            (nama, kehadiran, jumlah_tamu, ucapan, tanggal)
            VALUES (?, ?, ?, ?, ?)
        """, (
            nama,
            kehadiran,
            jumlah,
            ucapan,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

    return jsonify(status="success", pesan="Terima kasih, ucapan berhasil dikirim.")


if __name__ == "__main__":
    buat_database()
    app.run(debug=True)
