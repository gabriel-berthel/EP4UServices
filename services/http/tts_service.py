from EP4UServices.services.http.interfaces import RemoteTTSServiceBase

class RemotePiperTTS(RemoteTTSServiceBase):
    def __init__(self, url, endpoint = "", voice="en_US-ryan-high"):
        super().__init__(url, endpoint, voice)
        self.voice = voice
        
    def synthesize(self, speech):
        payload = {
            "voice": self.voice,
            "text": speech
        }
        
        return self.post(payload=payload).content
