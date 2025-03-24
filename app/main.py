import iot_api_client as iot
import api_utils as utils
from iot_api_client.exceptions import ApiException
from iot_api_client.configuration import Configuration
from iot_api_client.api import DevicesV2Api, ThingsV2Api ,PropertiesV2Api
from iot_api_client.models import ArduinoProperty
from pydantic import ValidationError



from time import sleep

import os
from dotenv import load_dotenv
import logging
import random
import string


# Load environment variables
load_dotenv()

# Secrets
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
THING_ID = os.getenv("THING_ID")
ORG_ID = os.getenv("ORG_ID")

ARDUINO_API_BASE_URL = "https://api2.arduino.cc/iot/v2"
TOKEN_URL = "https://api2.arduino.cc/iot/v1/clients/token"

# Activate loggin fro lib
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("requests_oauthlib")
logger.setLevel(logging.DEBUG)


# Configure API client
client_config = Configuration(host="https://api2.arduino.cc")
client = iot.ApiClient(client_config,header_name="X-Organization",header_value=ORG_ID)



# Function to list devices
@utils.exception_handler(client_config)
def get_things_for_org(org_id):
    api_instance = DevicesV2Api(client)
    api_response = api_instance.devices_v2_list(x_organization=org_id)
    for device in api_response:
        print(f"{device.name} - id:{device.id} - type:{device.type}")


# Get property for a thing
@utils.exception_handler(client_config)
def get_props_for_thing(thingID):
    properties_api = PropertiesV2Api(client)
    properties=properties_api.properties_v2_list(id=thingID, show_deleted=False)  
    return properties


# Loop to monitor and update things
@utils.exception_handler(client_config)
def monitor_and_update(known_properties: set):
    prop_result = get_props_for_thing(THING_ID)
    if prop_result == "retry":
        return prop_result
    current_property_ids = {prop.id for prop in prop_result}
    
    new_properties = current_property_ids - known_properties
    if new_properties:
        for property in prop_result:
            if property.id in new_properties:
                print(f"New properties detected for thing '{property.thing_name}': {new_properties}")
                print(f"Property: {property.name}::{property.type}={property.last_value}")
                result=update_prop_value(property,True) 
                if result == "retry":
                    return result
                if property.type == 'STATUS':
                    result=update_prop_name(property)
                    if result == "retry":
                        return result
                
    known_properties = current_property_ids
    return known_properties
   

@utils.exception_handler(client_config)     
def update_prop_value(property, value):
    if property.type=="STATUS":
        # example passing only optional values
        propertyValue = {"value": value}
        properties_api = PropertiesV2Api(client)
        api_response = properties_api.properties_v2_publish(THING_ID,property.id,propertyValue)
        return api_response

@utils.exception_handler(client_config)     
def random_string(length=10):
    characters = string.ascii_letters # Letters (upper & lower) + digits
    return ''.join(random.choice(characters) for _ in range(length))

@utils.exception_handler(client_config)     
def update_prop_name(property):  
    properties_api = PropertiesV2Api(client)
    propertyValue={"name":random_string(5),"permission":property.permission, "type":property.type,"update_strategy":property.update_strategy }
    properties_api.properties_v2_update(THING_ID,property.id,propertyValue)


if __name__ == "__main__":
    known_properties = set()
    while True:
        updated_set=monitor_and_update(known_properties)
        if updated_set!="retry":
            known_properties = updated_set
            sleep(10)
