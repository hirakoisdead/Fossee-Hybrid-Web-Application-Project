"""
API Client for communicating with Django backend.
"""

import requests
from typing import Optional, Dict, Any


class APIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api"):
        self.base_url = base_url
        self.token: Optional[str] = None
    
    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        return headers
    
    def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Register a new user."""
        response = requests.post(
            f"{self.base_url}/auth/register/",
            json={"username": username, "email": email, "password": password},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        self.token = data.get("token")
        return data
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login and obtain auth token."""
        response = requests.post(
            f"{self.base_url}/auth/login/",
            json={"username": username, "password": password},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        self.token = data.get("token")
        return data
    
    def logout(self):
        """Clear authentication."""
        self.token = None
    
    def is_authenticated(self) -> bool:
        return self.token is not None
    
    def upload_csv(self, file_path: str) -> Dict[str, Any]:
        """Upload a CSV file."""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        
        with open(file_path, 'rb') as f:
            response = requests.post(
                f"{self.base_url}/upload/",
                files={"file": f},
                headers=headers
            )
        response.raise_for_status()
        return response.json()
    
    def list_datasets(self) -> list:
        """Get list of user's datasets."""
        response = requests.get(
            f"{self.base_url}/datasets/",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_dataset(self, dataset_id: int) -> Dict[str, Any]:
        """Get dataset details."""
        response = requests.get(
            f"{self.base_url}/datasets/{dataset_id}/",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_summary(self, dataset_id: int) -> Dict[str, Any]:
        """Get dataset summary statistics."""
        response = requests.get(
            f"{self.base_url}/datasets/{dataset_id}/summary/",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def delete_dataset(self, dataset_id: int):
        """Delete a dataset."""
        response = requests.delete(
            f"{self.base_url}/datasets/{dataset_id}/",
            headers=self._get_headers()
        )
        response.raise_for_status()
    
    def download_report(self, dataset_id: int, save_path: str):
        """Download PDF report."""
        response = requests.get(
            f"{self.base_url}/datasets/{dataset_id}/report/",
            headers=self._get_headers()
        )
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)


# Global client instance
api_client = APIClient()
