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
            print(f"resp;:{data}")
            return data.get("success"), data.get("text"), data.get("plots")
        except requests.RequestException as e:
            logging.error(f"API Error: {str(e)}")
            return (
                False,
                "Sorry, there was an error connecting to the analysis service.",
                None,
            )

    def get_confidence_score(self, symbol: str) -> Tuple[bool, dict | str]:
        """
        Fetch get_confidence_score from the API
        Returns: (success, data)
        """
        try:
            response = requests.post(
                f"{self.base_url}/confidence_score",
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
                f"{self.base_url}/technical_analysis",
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
                f"{self.base_url}/crypto_info",
                json={"symbol": symbol},
                headers=self.headers,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("success"), data.get("text")
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
