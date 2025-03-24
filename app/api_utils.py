import json
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import os


# Secrets
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
THING_ID = os.getenv("THING_ID")
ORG_ID = os.getenv("ORG_ID")
ARDUINO_API_BASE_URL = "https://api2.arduino.cc/iot/v2"
TOKEN_URL = "https://api2.arduino.cc/iot/v1/clients/token"



# Create an OAuth2 session with automatic token refresh
oauth_client = BackendApplicationClient(client_id=CLIENT_ID)
oauth = OAuth2Session(client=oauth_client)

def exception_handler(client_config):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                token_refreshed = handle_api_exception(e,client_config)
                if token_refreshed:
                    return "retry"
                else :
                    return -1 
        return wrapper
    return decorator

def handle_api_exception(e, client_config):
    """Handles API exceptions, checks for token expiration, and refreshes token if needed."""
    if e.status == 401 or "token expired" in str(e).lower():
        print("Token expired. Refreshing token...")
        client_config.access_token = get_token()  # Call your token refresh function
        return True  # Indicate that the token was refreshed
    else:
        print(f"API Exception: {e}")
        return False  # Token was not expired, it's another error
    
# After updating the token you will most likely want to save it.
def get_token():
    token = oauth.fetch_token(
        token_url=TOKEN_URL,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        include_client_id=True,
        audience="https://api2.arduino.cc/iot",
        headers={"X-Organization": os.getenv("ORG_ID")},
    )
    return token.get("access_token")  