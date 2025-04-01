import docker



def run_chip_tool():    
    # Initialize Docker client
    client = docker.from_env()
    
    # Define container name and command
    container_name = "chip-tool"
    command = "mattertool startThread"
    command2 = "ot-ctl dataset active -x"
    
    try:
        # Get the container object
        container = client.containers.get(container_name)
    
        # Execute command inside the container
        exec_result = container.exec_run(command, tty=True, stdin=True)
    
        # Print output
        print(exec_result.output.decode())
        
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
    except Exception as e:
        print(f"Error: {e}")