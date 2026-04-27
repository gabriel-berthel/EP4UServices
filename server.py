
import hashlib
from io import BytesIO
import signal  #
import bottle
import torch
import pickle

from EP4UServices.services.local.piper_tts import LocalPiperTTS
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


from bottle import request, response
import json

@bottle.post('/tts')
def tts():
    try:
        data = request.json  # Bottle parses JSON automatically

        if not data:
            response.status = 400
            return {"error": "Invalid or missing JSON payload"}

        text = data.get("text")
        voice = data.get("voice")

        if not text:
            response.status = 400
            return {"error": "Missing 'text' field"}

        if not voice:
            response.status = 400
            return {"error": "Missing 'voice' field"}

        # Map voice name to model path (you define this)
        model_path = f"./voices/{voice}.onnx"

        tts_engine = LocalPiperTTS(model_path=model_path)

        audio_bytes = tts_engine.synthesize(text)

        response.content_type = 'audio/mpeg'
        return audio_bytes

    except Exception as e:
        response.status = 500
        return {"error": str(e)}

@bottle.post('/parse')
def parse_file():
    
    content = bottle.request.files.get("file")
    filename = f"document_tmp.pdf"
    
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