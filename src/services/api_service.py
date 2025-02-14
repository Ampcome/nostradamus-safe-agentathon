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
                f"{self.base_url}/addon/response",
                json={"query": query},
                headers=self.headers,
            )
            response.raise_for_status()
            data = response.json()
            print(f"resp;:{data}")
            return data.get("success"), data.get("text"), data.get("plots")
        except requests.RequestException as e:
            logging.error(f"API Error: {str(e)}")
            return (
                False,
                "Sorry, there was an error connecting to the analysis service.",
                None,
            )

    def get_plot_image(self, hash_string: str) -> Optional[bytes]:
        """
        Fetch plot image by hash string
        Returns: Image bytes if successful, None otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/addon/plot_image/{hash_string}", headers=self.headers
            )
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            logging.error(f"Error fetching plot image {hash_string}: {str(e)}")
            return None

    def get_confidence_score(self, symbol: str) -> Tuple[bool, dict | str]:
        """
        Fetch get_confidence_score from the API
        Returns: (success, data)
        """
        try:
            response = requests.post(
                f"{self.base_url}/addon/confidence_score",
                json={"symbol": symbol},
                headers=self.headers,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("success"), data.get("data")
        except requests.RequestException as e:
            logging.error(f"API Error: {str(e)}")
            return (
                False,
                "Sorry, there was an error connecting to the analysis service.",
            )

    def get_technical_analysis(self, symbol: str) -> Tuple[bool, dict | str]:
        """
        Fetch technical_analysi from the API
        Returns: (success, data)
        """
        try:
            response = requests.post(
                f"{self.base_url}/addon/technical",
                json={"symbol": symbol},
                headers=self.headers,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("success"), data.get("data")
        except requests.RequestException as e:
            logging.error(f"API Error: {str(e)}")
            return (
                False,
                "Sorry, there was an error connecting to the analysis service.",
            )

    def get_crypto_info(self, symbol: str) -> Tuple[bool, str]:
        """
        Fetch crypto_info from the API
        Returns: (success, text)
        """
        try:
            response = requests.post(
                f"{self.base_url}/addon/coin_info",
                json={"symbol": symbol},
                headers=self.headers,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("success"), data.get("data")
        except requests.RequestException as e:
            logging.error(f"API Error: {str(e)}")
            return (
                False,
                "Sorry, there was an error connecting to the analysis service.",
            )

    def get_price_info(self, symbol: str) -> Tuple[bool, dict | str]:
        """
        Fetch price_info from the API
        Returns: (success, data)
        """
        try:
            response = requests.post(
                f"{self.base_url}/addon/price_info",
                json={"symbol": symbol},
                headers=self.headers,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("success"), data.get("data")
        except requests.RequestException as e:
            logging.error(f"API Error: {str(e)}")
            return (
                False,
                "Sorry, there was an error connecting to the analysis service.",
            )
