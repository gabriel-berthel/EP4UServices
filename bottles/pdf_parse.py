from io import BytesIO

from bottle import Bottle, request, HTTPResponse, response
import subprocess
import os
import pickle

from services.docling_converter import DoclingConverter

app = Bottle()
IN_DIR = os.environ['IN_DIR']
OUT_DIR = os.environ['OUT_DIR']

converter = DoclingConverter()

@app.get("/parse/<file_id>")
def parse_file(file_id):
    file_id = os.path.basename(file_id)
    input_path = os.path.abspath(os.path.join(IN_DIR, file_id))
    output_path = os.path.abspath(os.path.join(OUT_DIR, file_id))

    print("Parsing file:", file_id)

    if not os.path.exists(input_path):
        return HTTPResponse(status=404, body=f"File {file_id} not found")

    try:
        result = converter.convert(input_path)

        mem_file = BytesIO()
        pickle.dump(result.document, mem_file)
        mem_file.seek(0)  # important, rewind to start

        # Set headers for download
        response.content_type = "application/octet-stream"
        response.set_header("Content-Disposition", f"attachment; filename={file_id}.pickle")

    except Exception as e:
        print("Error parsing:", e)
        return HTTPResponse(status=500, body="Error parsing file")

    return mem_file.getvalue()