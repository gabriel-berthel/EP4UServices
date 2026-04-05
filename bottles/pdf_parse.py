import datetime
import hashlib
from io import BytesIO
from datetime import datetime  #
from bottle import Bottle, request, HTTPResponse, response, run, post
import subprocess
import os
import pickle

from services.local.docling_converter import DoclingConverter

app = Bottle()

converter = DoclingConverter()

def hash_file_contents(contents: bytes) -> str:
    h = hashlib.sha256()
    h.update(contents)
    return h.hexdigest()

@post('/parse')
def parse_file():
    
    content = request.files.get("file")
    filename = f"document_.pdf"
    
    # Write bytes to file
    with open(filename, "wb") as f:
        f.write(content.file.read())
      
    if not content:
        return HTTPResponse(status=400, body="No file provided")

    try:
        result = converter.run(filename)

        mem_file = BytesIO()
        pickle.dump(result.document, mem_file)
        mem_file.seek(0)  # important, rewind to start

        # Set headers for download
        response.content_type = "application/octet-stream"
        response.set_header("Content-Disposition", f"attachment; filename={filename}.pickle")

    except Exception as e:
        print("Error parsing:", e)
        return HTTPResponse(status=500, body="Error parsing file")

    return mem_file.getvalue()

run(host='localhost', port=8080)