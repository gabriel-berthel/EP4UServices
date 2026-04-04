import json
from pathlib import Path
import re

from services.interfaces import LLMChatInterface, ParseInterface

class ServiceGateway:
    def __init__(self, parse_service:ParseInterface, chat_service: LLMChatInterface):
        self.parse_service = parse_service
        self.chat_service = chat_service


    def parse(self, file):
        if not self.parse_service:
            raise RuntimeError("Parse service not set")
        
        response = self.parse_service.run(file)
        
        filename='fallback.pickle'
        disposition = response.headers.get("Content-Disposition")
        if disposition:
            match = re.search(r'filename="?([^"]+)"?', disposition)
            if match:
                filename = match.group(1)
        
        with open(Path(filename), "wb") as f:
            f.write(response.content)
        
    
    def chat(self, user, system, json_resp: bool):
        if not self.chat_service:
            raise RuntimeError("Narration service not set")
        
        parameters = {
            'num_ctx': 4024*2,
            'stop_sequences': ["Remarks:"]
        }
        
        if json_resp:
            parameters['format'] = 'json'
        
        result = self.chat_service.run(user, system, parameters)
       
        if isinstance(result, dict):
            return result
        try:
            return json.loads(result)['message']['content']
        except (TypeError, json.JSONDecodeError):
            return {"error": "Invalid JSON returned", "raw": result}



