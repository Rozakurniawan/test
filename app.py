from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    env = os.getenv("ENV", "unknown")
    return f"Hello from {env} environment!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
