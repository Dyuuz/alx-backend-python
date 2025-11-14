import requests
from typing import Dict, Mapping, Sequence, Any

def get_json(url: str) -> Dict:
    """Get JSON from remote URL"""
    response = requests.get(url)
    return response.json()

