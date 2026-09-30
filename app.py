from flask import Flask, jsonify
import os

app = Flask(__name__)
DATA_DIR = "/data"
FILE_PATH = os.path.join(DATA_DIR, "clicks.txt")

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route("/", methods=["GET"])
def hello():
    # Write a log entry to the PVC to demonstrate persistent storage
    try:
        with open(FILE_PATH, "a") as f:
            f.write("Visited\n")
        with open(FILE_PATH, "r") as f:
            count = len(f.readlines())
    except Exception as e:
        count = f"Error: {str(e)}"

    return jsonify({
        "message": "Hello from Kubernetes Microservice!",
        "status": "healthy",
        "pvc_visit_count": count
    })

@app.route("/healthz", methods=["GET"])
def healthz():
    return jsonify({"status": "OK"}), 200

@app.route("/ready", methods=["GET"])
def ready():
    return jsonify({"status": "Ready"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
