# This file is part of the Python Arduino IoT Cloud.
# Any copyright is dedicated to the Public Domain.
# https://creativecommons.org/publicdomain/zero/1.0/
import time
import logging
from time import strftime
from arduino_iot_cloud import ArduinoCloudClient
from arduino_iot_cloud import Location
from arduino_iot_cloud import Schedule
from arduino_iot_cloud import ColoredLight
from arduino_iot_cloud import Task
from random import uniform
import argparse
import ssl # noqa
import os
from functools import partial
import time
import random
import chip_tool_interface as chip_tool
import re





KEY_PATH = "pkcs11:token=arduino"
CERT_PATH = "pkcs11:token=arduino"
CA_PATH = "ca-root.pem"


# Secrets
DEVICE_ID = os.getenv("DEVICE_ID")
SECRET_KEY = os.getenv("SECRET_KEY")





def on_switch_changed(client, value):
    # This is a write callback for the switch that toggles the LED variable. The LED
    # variable can be accessed via the client object passed in the first argument.
    client["led"] = value



if __name__ == "__main__":
    
    connected = False

    # Parse command line args.
    parser = argparse.ArgumentParser(description="arduino_iot_cloud.py")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debugging messages")
    parser.add_argument("-s", "--sync", action="store_true", help="Run in synchronous mode")
    args = parser.parse_args()

    # Assume the host has an active Internet connection.

    # Configure the logger.
    # All message equal or higher to the logger level are printed.
    # To see more debugging messages, pass --debug on the command line.
    logging.basicConfig(
        datefmt="%H:%M:%S",
        format="%(asctime)s.%(msecs)03d %(message)s",
        level=logging.DEBUG if args.debug else logging.INFO,
    )
    

    # Switch callback, toggles the LED.
    def on_switch_changed(client, value):
        # Note the client object passed to this function can be used to access
        # and modify any registered cloud object. The following line updates
        # the LED value.
        chip_tool.matter_onoff(THREAD_DATA_SET,"toggle","0x0000000000000001")
        client["led"] = value
    
    # Switch callback, toggles the LED.
    def message_receive(client, value):
        global connected

        # Note the client object passed to this function can be used to access
        # and modify any registered cloud object. The following line updates
        # the LED value.
        msg = client["message"]
        
        if msg == "THREAD_DATA_SET":
            client["message"] = THREAD_DATA_SET
        elif "pin" in msg:
            # Use regex to find all digits
            pin = re.split(" ",msg)
            output = chip_tool.connect_to_device(THREAD_DATA_SET,pin[1])
            print(output)
            if "Error" in output:
                client["message"] = "Unable to connect to end device"
            else:
                pattern = r'node ID ([0x0-9A-Fa-f]+)'
                # Search for the node ID in the log data
                node_id = re.search(pattern, output)
                result = f"Connected to Node ID: {node_id.group(1)}"
                connected = True
                client["message"] = result
        elif msg == "\x1b":
            return   
        elif msg == "Start" and THREAD_DATA_SET == None:
            client["message"] = "Start Chip Tool failed.."
        elif msg == "Start" and THREAD_DATA_SET != None:
            client["message"] = "Thread Network successfully started"
        elif msg == "SetConnected" and THREAD_DATA_SET != None:
            client["message"] = "Connected"
            connected = True
        else: 
            client["message"] = "receive"

       
     

        
    def value_update(client, value):
        print(client["temperature"])
        

    def generate_random_variable(connected):
        # random_var = random.uniform(1.0, 100.0)  # Generate a random number between 1 and 100
        # print(random_var)
        # return random_var   
        if THREAD_DATA_SET != None and connected==True:          
            output=chip_tool.read_value("0x0000000000000001")
            if output != None:
                print(output)
                match = re.search(r'MeasuredValue:\s*(\d+)', output)
                # If a match is found, capture the value as a float
                if match:
                    measured_value = float(match.group(1))
                    val = measured_value/100.0
                    print(val)
                    return val 
                else:
                    print("No match found.")
                    return 0.0
    
     
    THREAD_DATA_SET = chip_tool.start_chip_tool()

    # 1. Create a client object, which is used to connect to the IoT cloud and link local
    # objects to cloud objects. Note a username and password can be used for basic authentication
    # on both CPython and MicroPython. For more advanced authentication methods, please see the examples.
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

    # 2. Register cloud objects.
    # Note: The following objects must be created first in the dashboard and linked to the device.
    # When the switch is toggled from the dashboard, the on_switch_changed function is called with
    # the client object and new value args.
    client.register("smartPlug", value=False, on_write=on_switch_changed,  interval=0.250)
    
    # The LED object is updated in the switch's on_write callback.
    client.register("led", value=False)
    client.register("message", value=None, on_write=message_receive,interval=0.250)  
    client.register("temperature", value=None, on_read=lambda _: generate_random_variable(connected), interval=1.0)
    client.register("vibration", value=None, on_read=lambda _: generate_random_variable(connected), interval=2.0)


    # 3. Start the Arduino cloud client.
    client.start()
    

    
    # mattertool temperaturemeasurement read measured-value 0x0000000000000001 0x04 | grep -i MeasuredValue
    # mattertool onoff read on-off 0x0000000000001F24 0x03 | grep -i OnOff:
    # pin 34970112332
    
    
