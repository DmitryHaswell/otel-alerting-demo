import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Manual Metrics Registry ---
# As an SRE, think of this as your in-memory TSDB
metrics_db = {
    "requests_total": 0,    # Rate
    "errors_total": 0,      # Errors
    "durations": []         # Duration (Raw samples for a simple average/max)
}

@app.before_request
def start_timer():
    # Store the start time on the 'request' object (thread-local in Flask)
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    # 1. Increment Rate
    metrics_db["requests_total"] += 1
    
    # 2. Increment Errors (Anything in the 5xx range)
    if 500 <= response.status_code <= 599:
        metrics_db["errors_total"] += 1
    
    # 3. Record Duration
    latency = time.time() - request.start_time
    metrics_db["durations"].append(latency)
    
    return response

# --- Endpoints ---

@app.route("/")
def hello():
    return "The app just did something."

@app.route("/error")
def trigger_error():
    # Simulate a server failure
    return "Something went wrong!", 500

@app.route("/slow")
def slow_request():
    # Simulate latency
    time.sleep(0.5)
    return "This took quite a while!"

@app.route("/metrics")
def get_metrics():
    """
    Reporting endpoint
    """
    count = metrics_db["requests_total"]
    avg_latency = (sum(metrics_db["durations"]) / count) if count > 0 else 0
    
    # Returning a structured JSON for your demo
    return jsonify({
        "rate": {
            "total_requests": count
        },
        "errors": {
            "total_errors": metrics_db["errors_total"],
            "error_rate_percent": (metrics_db["errors_total"] / count * 100) if count > 0 else 0
        },
        "duration": {
            "avg_latency_seconds": round(avg_latency, 4),
            "last_latency_seconds": round(metrics_db["durations"][-1], 4) if metrics_db["durations"] else 0
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)