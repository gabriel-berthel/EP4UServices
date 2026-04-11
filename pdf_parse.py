
import hashlib
from io import BytesIO
import signal  #
import bottle
import torch
import pickle

from services.local.docling_converter import DoclingParseService

app = bottle.Bottle()

converter = DoclingParseService()

def hash_file_contents(contents: bytes) -> str:
    h = hashlib.sha256()
    h.update(contents)
    return h.hexdigest()

def cleanup(signum, frame):
    print("\nSignal received, cleaning up GPU memory...")
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()
    print("Cleanup done. Exiting.")
    exit(0)

# Register handlers
signal.signal(signal.SIGINT, cleanup)   # Ctrl+C
signal.signal(signal.SIGTERM, cleanup)  # kill <PID>


@bottle.post('/parse')
def parse_file():
    
    content = bottle.request.files.get("file")
    filename = f"document_.pdf"
    
    # Write bytes to file
    with open(filename, "wb") as f:
        f.write(content.file.read())
      
    if not content:
        return bottle.HTTPResponse(status=400, body="No file provided")
    
    try:
        result = converter.parse(filename)

        mem_file = BytesIO()
        pickle.dump(result.document, mem_file)
        mem_file.seek(0)  # important, rewind to start

        # Set headers for download
        bottle.response.content_type = "application/octet-stream"
        bottle.response.set_header("Content-Disposition", f"attachment; filename={filename}.pickle")

    except Exception as e:
        print("Error parsing:", e)
        return bottle.HTTPResponse(status=500, body="Error parsing file")

    return mem_file.getvalue()


if __name__ == '__main__':
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()
    bottle.run(host='localhost', port=8080)