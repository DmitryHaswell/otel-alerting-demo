import time
import random
from flask import Flask, request, jsonify

# OTel Imports
from opentelemetry import metrics
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)

# --- OpenTelemetry Setup ---
# 1. Identity: Give your service a name for the collector to see
resource = Resource(attributes={SERVICE_NAME: "flask-demo-service"})

# 2. Export: Send metrics to the collector at localhost:4317 (gRPC)
exporter = OTLPMetricExporter(endpoint="http://localhost:4317", insecure=True)
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)

# 3. Provider: Glue everything together
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)

# 4. Instrumentation: This captures the RED metrics automatically
FlaskInstrumentor().instrument_app(app)

# --- Keep your existing logic ---
CHAOS_CONFIG = {
    "error_rate": 0.25,
    "slow_rate": 0.15,
    "slow_delay_sec": 2.0
}

metrics_db = {"requests_total": 0, "errors_total": 0, "durations": []}

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    metrics_db["requests_total"] += 1
    if 500 <= response.status_code <= 599:
        metrics_db["errors_total"] += 1
    metrics_db["durations"].append(time.time() - request.start_time)
    return response

@app.route("/")
def hello():
    if random.random() < CHAOS_CONFIG["slow_rate"]:
        time.sleep(CHAOS_CONFIG["slow_delay_sec"])
    if random.random() < CHAOS_CONFIG["error_rate"]:
        return "Internal Server Error", 500
    return "Hello, world!"

@app.route("/metrics")
def get_metrics():
    # Your manual verification endpoint
    return jsonify({"manual_metrics": metrics_db})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)