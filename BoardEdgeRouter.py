import iot_api_client as iot
from iot_api_client.exceptions import ApiException
from iot_api_client.configuration import Configuration
from iot_api_client.api import DevicesV2Api, ThingsV2Api ,PropertiesV2Api
from iot_api_client.models import ArduinoProperty
from pydantic import ValidationError



from time import sleep
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv
import logging
import random
import string


# Load environment variables
load_dotenv()

# Constants
ARDUINO_API_BASE_URL = "https://api2.arduino.cc/iot/v2"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
THING_ID = os.getenv("THING_ID")
ORG_ID = os.getenv("ORG_ID")
TOKEN_URL = "https://api2.arduino.cc/iot/v1/clients/token"

# Activate loggin fro lib
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("requests_oauthlib")
logger.setLevel(logging.DEBUG)


# After updating the token you will most likely want to save it.
def get_token(client) :
    token = oauth.fetch_token(
        token_url=TOKEN_URL,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        include_client_id=True,
        audience="https://api2.arduino.cc/iot",
        headers={"X-Organization": ORG_ID},
    )
    # Extract access token
    access_token = token.get("access_token")
    client_config.access_token = access_token    





# Create an OAuth2 session with automatic token refresh
oauth_client = BackendApplicationClient(client_id=CLIENT_ID)
oauth = OAuth2Session(client=oauth_client)
# Configure API client
client_config = Configuration(host="https://api2.arduino.cc")
client = iot.ApiClient(client_config,header_name="X-Organization",header_value=ORG_ID)

get_token(client)


# Function to list devices
def get_things_for_org(org_id):
    try:
        api_instance = DevicesV2Api(client)
        api_response = api_instance.devices_v2_list(x_organization=org_id)
        for device in api_response:
            print(f"{device.name} - id:{device.id} - type:{device.type}")

    except ApiException as e:
        print(f"Exception when calling DevicesV2Api->devices_v2_list: {e}")
        get_token(client)



def get_props_for_thing(thingID):
    try:
        properties_api = PropertiesV2Api(client)
        properties=properties_api.properties_v2_list(id=thingID, show_deleted=False)  
        return properties
    
    except ApiException as e:
        print(f"Exception when calling DevicesV2Api->devices_v2_list: {e}")
        get_token(client)
        return None

# Loop to monitor and update things
def monitor_and_update():
    known_properties = set()
    while True:
        properties = get_props_for_thing(THING_ID)
        if properties == None:
            continue
        current_property_ids = {prop.id for prop in properties}
        
        new_properties = current_property_ids - known_properties
        if new_properties:
            for property in properties:
                if property.id in new_properties:
                    print(f"New properties detected for thing '{property.thing_name}': {new_properties}")
                    print(f"Property: {property.name}::{property.type}={property.last_value}")
                    result=update_prop_value(property,True)  
                    if result == "retry":
                        continue
                    if property.type == 'STATUS':
                        update_prop_name(property)
                    
        known_properties = current_property_ids
        sleep(10)  # Adjust sleep time to avoid rate limiting
        
def update_prop_value(property, value):
    if property.type=="STATUS":
        # example passing only optional values
        propertyValue = {"value": value}
        try:
            properties_api = PropertiesV2Api(client)
            api_response = properties_api.properties_v2_publish(THING_ID,property.id,propertyValue)
            return api_response
        except iot.ApiException as e:
            print(f"An error occurred: {e}")
            get_token(client)
            return "retry"


def random_string(length=10):
    characters = string.ascii_letters # Letters (upper & lower) + digits
    return ''.join(random.choice(characters) for _ in range(length))


def update_prop_name(property):  
    try:
        properties_api = PropertiesV2Api(client)
        propertyValue={"name":random_string(5),"permission":property.permission, "type":property.type,"update_strategy":property.update_strategy }
        properties_api.properties_v2_update(THING_ID,property.id,propertyValue)
    except iot.ApiException as e:
        print(f"An error occurred: {e}")
        get_token(client)
        return None

if __name__ == "__main__":
    monitor_and_update()
