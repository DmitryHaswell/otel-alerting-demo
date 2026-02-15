import requests
import time
import sys

# CONFIGURATION
TARGET_URL = "http://localhost:8000/"
REQUESTS_PER_SECOND = 2 

print(f"Starting traffic generator -> {TARGET_URL}")
print(f"Rate: {REQUESTS_PER_SECOND} req/sec. Press Ctrl+C to stop.")

try:
    while True:
        try:
            start_time = time.time()
            response = requests.get(TARGET_URL, timeout=5)
            
            status = "OK" if response.status_code == 200 else f"ERROR: {response.status_code}"
            print(f"[{time.strftime('%H:%M:%S')}] {status}")
            
        except requests.exceptions.RequestException as e:
            print(f"Connection Error: {e}")

        # Maintain the configured rate
        time.sleep(1 / REQUESTS_PER_SECOND)

except KeyboardInterrupt:
    print("\nStopping traffic. Demo over!")
    sys.exit(0)