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

def wrapper(s: str) -> str:
    """
    Wraps a given string to fit within a fixed width suitable for an 80mm printer.

    This function takes a string 's' and formats it so that each line does not exceed
    48 characters. This character limit is chosen based on the printing capabilities of an
    80mm printer, ensuring that the text is properly wrapped at word boundaries.

    The function splits the input string into words and accumulates them in a new string,
    inserting a newline character when adding another word would exceed the 48-character limit.
    If the string is shorter than or equal to 48 characters, a newline is simply appended.

    Args:
        s (str): The string to be wrapped for printing.

    Returns:
        str: The formatted string with newline characters inserted at appropriate positions.
    """
    n = len(s)
    count = 0
    new_s = ""
    
    # If the string exceeds the length limit, perform word wrapping.
    if n > 48:
        for word in s.split(' '):
            
            if (count + len(word) + 1) < 48:
                new_s += word + " "
                count += len(word) + 1  # Update the count with the length of the word and a space.
            else:
                new_s += "\n"
                count = 0
        
        return new_s
    # If the string is within the limit, simply append a newline at the end.
    s += "\n"
    return s
