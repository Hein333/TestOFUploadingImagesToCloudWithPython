import os
import oci
from flask import Flask, render_template

app = Flask(__name__)

# Load OCI configuration from Environment Variables (set in Render dashboard)
config = {
    "user": os.environ.get("OCI_USER"),
    "key_content": os.environ.get("OCI_KEY_CONTENT"),
    "fingerprint": os.environ.get("OCI_FINGERPRINT"),
    "tenancy": os.environ.get("OCI_TENANCY"),
    "region": os.environ.get("OCI_REGION", "us-ashburn-1")
}

NAMESPACE = os.environ.get("OCI_NAMESPACE")
BUCKET_NAME = os.environ.get("OCI_BUCKET_NAME")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
