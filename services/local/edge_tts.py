

import asyncio
import os
import tempfile
import edge_tts

from EP4UServices.services.core import AsyncTTSEngineInterface, TTSEngineInterface


class LocalEdgeTTS(TTSEngineInterface):
    """
    CAREFUl! This is using microsoft remote services :)
    
    Use for online ressources OR Q/A kinda interactions.
    """
    
    def synthesize(self, speech: str) -> bytes:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        path = tmp.name
        tmp.close()

        try:
            communicate = edge_tts.Communicate(
                text=speech,
                voice="en-US-JennyNeural"
            )

            communicate.save_sync(path)

            with open(path, "rb") as f:
                audio_bytes = f.read()

            return audio_bytes

        finally:
            os.remove(path)
            
class AsyncLocalEdgeTTS(AsyncTTSEngineInterface):
    """
    CAREFUl! This is using microsoft remote services :)
    
    Use for online ressources OR Q/A kinda interactions.
    """
    
    async def synthesize(self, speech: str) -> bytes:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        path = tmp.name
        tmp.close()

        try:
            communicate = edge_tts.Communicate(
                text=speech,
                voice="en-US-JennyNeural"
            )

            await communicate.save(path)

            with open(path, "rb") as f:
                audio_bytes = f.read()

            return audio_bytes

        finally:
            os.remove(path)
       
       
from pydub import AudioSegment
from piper import PiperVoice
import io
import wave
from piper import PiperVoice
from pydub import AudioSegment


class LocalPiperTTS(TTSEngineInterface):
    """
    Piper TTS (fully in-memory)
    Contract: returns MP3 bytes
    """

    def __init__(self, model_path: str, use_cuda: bool = False):
        self.voice = PiperVoice.load(model_path, use_cuda=use_cuda)

    def synthesize(self, text: str) -> bytes:
        return self._render(text)

    def _render(self, text: str) -> bytes:
        # 1. In-memory WAV buffer
        wav_buffer = io.BytesIO()

        with wave.open(wav_buffer, "wb") as wav_file:
            self.voice.synthesize_wav(text, wav_file)

        # IMPORTANT: reset pointer
        wav_buffer.seek(0)

        # 2. Decode WAV in-memory → AudioSegment
        audio = AudioSegment.from_file(wav_buffer, format="wav")

        # 3. Encode to MP3 in-memory
        mp3_buffer = io.BytesIO()
        audio.export(mp3_buffer, format="mp3")

        return mp3_buffer.getvalue()