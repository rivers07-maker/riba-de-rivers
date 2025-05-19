from dotenv import load_dotenv
import requests
import os
import json
from ..utils import load_configuration

# Load environment variables
load_configuration()

HOSTHUB_KEY = os.getenv("HOSTHUB_KEY")
HOSTHUB_RENTAL_ID = os.getenv("HOSTHUB_RENTAL_ID")

class HostHubAPI:
    def __init__(self):
        self.base_url = "https://app.hosthub.com/api/2019-03-01"
        self.headers = {
            "Authorization": f"{HOSTHUB_KEY}",
            "Content-Type": "application/json"
        }
    
    def create_temporary_booking(self, type="Hold", date_from= "<date>", date_to= "<date>"):
        url = f"{self.base_url}/rentals/{HOSTHUB_RENTAL_ID}/calendar-events"
        response = requests.post(url, headers=self.headers, data=json.dumps({
            "type": type,
            "date_from": date_from,
            "date_to": date_to
        }))
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error creating temporary booking: {response.text}")
    
hosthub = HostHubAPI()