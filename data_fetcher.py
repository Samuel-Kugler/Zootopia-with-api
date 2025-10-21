import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


URL = "https://api.api-ninjas.com/v1/animals"
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    print("Warning: No API key found! Please add it to your .env file.")


def fetch_data(animal_name: str) -> list[dict]:
    """
    Fetches the animals data for the animal 'animal_name'.
     Returns: a list of animals, each animal is a dictionary:
        {
        'name': ...,
        'taxonomy': {
          ...
          }
        ,
        'locations': [
          ...
        ],
        'characteristics': {
          ...
        }
      },
    """
    try:
        response = requests.get(URL, params={"name": animal_name}, headers={"x-api-key": API_KEY}, timeout=10)
        response.raise_for_status()
        json_file = response.json()

    except requests.ConnectionError:
        return [{"name": "Error!", "characteristics": {"type": "Connection failed."}}]
    except requests.Timeout:
        return [{"name": "Error!", "characteristics": {"type": "Request timed out."}}]
    except requests.HTTPError as e:
        return [{"name": "Error!", "characteristics": {"type": f"HTTP error: {e}"}}]
    except requests.RequestException as e:
        return [{"name": "Error!", "characteristics": {"type": f"Request failed: {e}"}}]
    except UnicodeDecodeError:
        return [{"name": "Error!", "characteristics": {"type": "Response encoding problem."}}]
    except json.JSONDecodeError:
        return [{"name": "Error!", "characteristics": {"type": "Response is not valid JSON."}}]
    except PermissionError:
        return [{"name": "Error!", "characteristics": {"type": "Missing Permission."}}]
    except OSError as e:
        return [{"name": "Error!", "characteristics": {"type": f"Some other OS Error: {e}"}}]

    return json_file
