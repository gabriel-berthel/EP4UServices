import hashlib
from io import BytesIO

from bottle import Bottle, request, HTTPResponse, response
import subprocess
import os
import pickle

from EP4UServices.services.local.docling_converter import DoclingConverter

app = Bottle()

converter = DoclingConverter()

def hash_file_contents(contents: bytes) -> str:
    h = hashlib.sha256()
    h.update(contents)
    return h.hexdigest()


@app.put("/parse")
def parse_file():
    
    upload = request.files.get("file")
    content = upload.read()

    if not upload:
        return HTTPResponse(status=400, body="No file provided")
    
    file_bytes = content.file.read()
    file_hash = hash_file_contents(file_bytes)[:24]     

    try:
        result = converter.convert(file_bytes)

        mem_file = BytesIO()
        pickle.dump(result.document, mem_file)
        mem_file.seek(0)  # important, rewind to start

        # Set headers for download
        response.content_type = "application/octet-stream"
        response.set_header("Content-Disposition", f"attachment; filename={file_hash}.pickle")

    except Exception as e:
        print("Error parsing:", e)
        return HTTPResponse(status=500, body="Error parsing file")

    return mem_file.getvalue()