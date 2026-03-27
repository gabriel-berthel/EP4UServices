from bottle import Bottle, request, HTTPResponse, static_file
import os, hashlib, pickle

app = Bottle()

# Directories
IN_DIR = os.environ['IN_DIR']
OUT_DIR = os.environ['OUT_DIR']
os.makedirs(IN_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# --- Utility: hash file contents ---
def hash_file_contents(contents: bytes) -> str:
    h = hashlib.sha256()
    h.update(contents)
    return h.hexdigest()

def save_uploaded_file(file_bytes: bytes, filename: str = None) -> str:
    file_hash = hash_file_contents(file_bytes)
    
    file_path = os.path.join(IN_DIR, file_hash)
    with open(file_path, "wb") as f:
        f.write(file_bytes)
    
    return os.path.basename(file_path)

# --- Upload endpoint ---
@app.post("/upload")
def upload_file():
    upload = request.files.get("file")
    if not upload:
        return HTTPResponse(status=400, body="No file provided")

    file_bytes = upload.file.read()
    file_id = save_uploaded_file(file_bytes, upload.filename)[:32]
    
    return {"file_id": file_id}

# --- Download endpoint ---
@app.get("/download/<file_id>")
def download_file(file_id):
    file_path = os.path.join(OUT_DIR, file_id)
    if not os.path.exists(file_path):
        return HTTPResponse(status=404, body="File not found")
    
    return static_file(file_id, root=OUT_DIR, download=file_id)
