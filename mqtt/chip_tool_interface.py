import docker
import re


THREAD_DATA_SET = ""

chip_too_c = "chip-tool"
otbr_c = "otbr"
# Initialize Docker client
client = docker.from_env()



def start_chip_tool():    

    # Define container name and command
    command = "mattertool startThread"
    command2 = "ot-ctl dataset active -x"
    
    try:
        # Get the container object
        container = client.containers.get(chip_too_c)
    
        # Execute command inside the container
        exec_result = container.exec_run(command, tty=True, stdin=True)
    
        # Print output
        print(exec_result.output.decode())
        
        container = client.containers.get(otbr_c)

        
        # Run the command inside the container
        exec_result2 = container.exec_run(command2)

        # Get the output from the exec_run command
        output2 = exec_result2.output.decode()

        # Clean up the output using sed equivalents in Python
        cleaned_output = output2.splitlines()[0].replace('\r', '')

        # Set the environment variable in Python (to simulate export)
        THREAD_DATA_SET = cleaned_output

        # Print the result (you can use THREAD_DATA_SET in your code)
        print(f"THREAD_DATA_SET: {THREAD_DATA_SET}")
        return THREAD_DATA_SET
    except Exception as e:
        print(f"Error: {e}")
        
        
def connect_to_device(th_set,pin):
    command3 = f"chip-tool pairing code-thread 1 hex:{th_set} {pin}"
    try:
        container3 = client.containers.get(chip_too_c)
        
        # Execute command inside the container
        exec_result3 = container3.exec_run(command3)
        
        
        # Get the output from the exec_run command
        output3 = exec_result3.output.decode()
        
        
        return output3
 
    except Exception as e:
        print(f"Error: {e}")
        
        
def matter_onoff(th_set,mode, matter_code):
    command = f"chip-tool onoff {mode} {matter_code} 0x03"
    try:
        container = client.containers.get(chip_too_c)
        
        # Execute command inside the container
        exec_result = container.exec_run(command)
        
        
        # Get the output from the exec_run command
        output = exec_result.output.decode()
        
        
        return output
 
    except Exception as e:
        print(f"Error: {e}")
        

def read_value(matter_code):
    command = f"chip-tool temperaturemeasurement read measured-value {matter_code} 0x04"
    try:
        container = client.containers.get(chip_too_c)
        
        # Execute command inside the container
        exec_result = container.exec_run(command)
        
        
        # Get the output from the exec_run command
        output = exec_result.output.decode()
        
        
        return output
 
    except Exception as e:
        print(f"Error: {e}")
    
    
    
