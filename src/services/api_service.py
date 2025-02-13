import logging
from typing import Optional, Tuple

import requests

from src.core.cofig import settings


class AnalysisAPIService:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.api_key = settings.API_KEY
        self.headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}

    def get_analysis(self, query: str) -> Tuple[bool, str, Optional[str]]:
        """
        Fetch analysis from the API
        Returns: (success, text, plots)
        """
        try:
            response = requests.post(
                f"{self.base_url}/chat/response",
                json={"query": query},
                headers=self.headers,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("success"), data.get("text"), data.get("plots")
        except requests.RequestException as e:
            logging.error(f"API Error: {str(e)}")
            return (
                False,
                "Sorry, there was an error connecting to the analysis service.",
                None,
            )
