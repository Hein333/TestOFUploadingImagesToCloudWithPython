import os
import oci
from flask import Flask, render_template

app = Flask(__name__)

# Load OCI configuration from Environment Variables
NAMESPACE = os.environ.get("OCI_NAMESPACE")
BUCKET_NAME = os.environ.get("OCI_BUCKET_NAME")
REGION = os.environ.get("OCI_REGION", "us-ashburn-1")

@app.route("/")
def index():
    # 1. Have Python construct the OCI image URL dynamically
    image_filename = "logo.png"  # The name of the file inside your OCI bucket
    
    # Standard OCI public URL format
    oci_image_url = f"https://objectstorage.{REGION}.oraclecloud.com/p/{NAMESPACE}/b/{BUCKET_NAME}/o/{image_filename}"
    
    # 2. Pass the Python variable into the HTML template
    return render_template("index.html", image_url=oci_image_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
