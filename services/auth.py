import time
import requests


from app.settings import USERNAME, PASSWORD, MAX_ATTEMPTS, AUTH_URL, RETRY_DELAY

def get_auth_tokens() -> tuple:
    """
    Retrieves authentication tokens from the authorization server.

    This function attempts to authenticate using predefined USERNAME and PASSWORD credentials,
    and obtains an access token from an authorization endpoint. It will try to send the authentication
    request up to MAX_ATTEMPTS times if needed, handling common HTTP errors and exceptions.

    Returns:
        tuple: A tuple containing:
            - success_status (bool): True if the token was successfully retrieved, otherwise False.
            - access_token (str): The retrieved access token if successful; otherwise, an empty string.
            - error_message (str): An error message if the request failed; otherwise, an empty string.

    Behavior:
      - If either USERNAME or PASSWORD is not provided, returns a failure tuple with an appropriate error message.
      - Sends a POST request to the AUTH_URL with the credentials.
      - On a successful response (HTTP 200), extracts the 'access' token from the JSON response.
      - If the token is missing in the response, returns an error message indicating the absence of the access token.
      - Specifically handles HTTP 401 errors (invalid credentials) and HTTP 500+ errors (server issues) with retries.
      - Waits for a specified RETRY_DELAY between retries for server errors or exceptions.
      - Returns a failure tuple if an unexpected error occurs or if all attempts are exhausted.
    """
    if not USERNAME and not PASSWORD:
        return (False, "", "Faltam as credênciais do usuário.")
    
    json = {
        "username" : USERNAME,
        "password" : PASSWORD
    }

    for attempt in range(1, MAX_ATTEMPTS):
        try:
            response = requests.post(
                AUTH_URL,
                json=json,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            print(json, AUTH_URL)

            if response.status_code == 200:
                access_token = response.json().get('access')
                if access_token:
                    return (True, access_token, "")
                return (False, "", "Falta o token de acesso na responsta.")
            
            # Handle HTTP errors
            if response.status_code == 401:
                return (False, "", f"Credênciais de Autenticação Inválidas.")
            
            if response.status_code >= 500:
                time.sleep(RETRY_DELAY)
                continue

            return (False, "", f"Resposta Inesperada: {response.status_code} {response.text}")

        except requests.exceptions.RequestException as e:
            time.sleep(RETRY_DELAY)
        except Exception as e:
            return (False, "", f'erro inesperado: {str(e)}')
    
    return (False, "", f"Problema com autenticação no servidor.")