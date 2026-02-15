import time
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# CONFIGURATION
CHAOS_CONFIG = {
    "error_rate": 0.25,      # 25% of requests will fail with a 500
    "slow_rate": 0.15,       # 15% of requests will be slow
    "slow_delay_sec": 2.0    # How long 'slow' requests take
}

# --- Manual metrics storage ---
metrics_db = {
    "requests_total": 0,    # Rate
    "errors_total": 0,      # Errors
    "durations": []         # Duration (Raw samples for a simple average/max)
}

@app.before_request
def start_timer():
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
    # --- Chaos Logic ---
    # 1. Simulate Latency
    if random.random() < CHAOS_CONFIG["slow_rate"]:
        time.sleep(CHAOS_CONFIG["slow_delay_sec"])

    # 2. Simulate Errors
    if random.random() < CHAOS_CONFIG["error_rate"]:
        return "Internal Server Error", 500
    
    return "Hello, world!"

@app.route("/metrics")
def get_metrics():
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
            "avg_latency_seconds": round(avg_latency, 4)
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)