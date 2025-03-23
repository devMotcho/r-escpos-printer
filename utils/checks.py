import requests
from app.settings import MAX_ATTEMPTS

def check_url(url: str) -> bool:
    """
    Check if a given URL is reachable by sending HTTP GET requests.

    This function attempts to connect to the provided URL up to 5 times. If a successful 
    response (HTTP status code 200) is received within these attempts, it returns True. 
    Otherwise, it returns False. The function handles network-related exceptions gracefully 
    by catching them and returning False if any occur.

    Args:
        url (str): The URL to be checked.

    Returns:
        bool: True if the URL is reachable (status code 200 received), False otherwise.
    """
    counter = 0
    status = False
    
    # Attempt to get a successful response.
    try:
        while not status and counter < MAX_ATTEMPTS:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                status = True
            counter += 1
    except requests.exceptions.RequestException:
        return False
    
    return status

