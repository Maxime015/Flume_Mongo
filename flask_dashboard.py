from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["flume_logs"]
collection = db["logs"]

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/data")
def api_data():
    try:
        minutes = int(request.args.get("minutes", 10))  # par défaut 10 min
    except ValueError:
        minutes = 10

    cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)

    # 🟡 Filtrage basé sur la date en UTC (MongoDB stocke souvent en UTC)
    cursor = collection.find({
        "timestamp": {"$gte": cutoff_time.isoformat()}
    })

    buckets = defaultdict(int)
    status_counts = defaultdict(int)

    for doc in cursor:
        ts = doc.get("timestamp")
        status = doc.get("status", "unknown")
        try:
            dt = datetime.fromisoformat(ts)
            if dt >= cutoff_time:  # sécurité supplémentaire
                bucket = dt.strftime("%Y-%m-%d %H:%M")
                buckets[bucket] += 1
                status_counts[status] += 1
        except Exception:
            continue

    return jsonify({
        "time_buckets": dict(sorted(buckets.items())),
        "status_counts": dict(status_counts)
    })

if __name__ == "__main__":
    app.run(debug=True)
