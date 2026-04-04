
from dataclasses import dataclass
import requests
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class HTTPClient(ABC):
    def __init__(self, url: str, endpoint: str = "/"):
        self.url = url.rstrip("/")  # normalize base URL
        self.endpoint = endpoint

    def get(self, url_params = str|None, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        GET request to self.url + endpoint with optional query parameters.
        """
        

        full_url = f"{self.url}/{self.endpoint.lstrip('/')}"
        if url_params:
            full_url += f"/{url_params.lstrip('/')}"
        
        print(full_url)
        
        response = requests.get(full_url, params=params)
        # response.raise_for_status()  # raise exception on HTTP error
        return response

    def post(self, payload: Optional[Dict[str, Any]] = None, file: Optional[str] = None) -> requests.Response:
        """
        Perform a POST request to self.url + endpoint.
        If 'file' is provided, sends it as multipart/form-data under key 'file'.
        """
        full_url = f"{self.url}/{self.endpoint.lstrip('/')}"
        files = None
        if file:
            files = {"file": open(file, "rb")}
        try:
            response = requests.post(full_url, json=payload, files=files)
            response.raise_for_status()
            return response
        finally:
            if files:
                files["file"].close()

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Abstract method to be implemented by subclasses.
        """
        pass