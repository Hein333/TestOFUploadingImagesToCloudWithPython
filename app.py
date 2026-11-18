import os
import oci
from flask import Flask, render_template, request

app = Flask(__name__)

# Load OCI configuration from Environment Variables
NAMESPACE = os.environ.get("OCI_NAMESPACE")
BUCKET_NAME = os.environ.get("OCI_BUCKET_NAME")
REGION = os.environ.get("OCI_REGION", "us-ashburn-1")

# Initialize OCI Client using Render environment variables
config = {
    "user": os.environ.get("OCI_USER"),
    "key_content": os.environ.get("OCI_KEY_CONTENT"),
    "fingerprint": os.environ.get("OCI_FINGERPRINT"),
    "tenancy": os.environ.get("OCI_TENANCY"),
    "region": REGION
}

object_storage_client = oci.object_storage.ObjectStorageClient(config)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_image():
    # 1. Check if an image file was included in the form request
    if "image_file" not in request.files:
        return render_template("index.html", message="No file part in the request.")
    
    file = request.files["image_file"]
    
    if file.filename == "":
        return render_template("index.html", message="No selected file.")
    
    if file:
        filename = file.filename
        
        try:
            # 2. Upload the file stream directly to OCI Object Storage
            object_storage_client.put_object(
                namespace_name=NAMESPACE,
                bucket_name=BUCKET_NAME,
                object_name=filename,
                put_object_body=file.stream
            )
            
            # 3. Construct the public URL to display the image back to the user
            oci_image_url = f"https://objectstorage.{REGION}.oraclecloud.com/p/{NAMESPACE}/b/{BUCKET_NAME}/o/{filename}"
            
            return render_template("index.html", message=f"Successfully uploaded '{filename}' to Oracle Cloud!", image_url=oci_image_url)
            
        except Exception as e:
            return render_template("index.html", message=f"Upload failed: {str(e)}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
