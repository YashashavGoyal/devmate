import sys
import os
sys.path.append(os.getcwd())

from python_on_whales import docker, DockerClient

def debug():
    # We need a dummy compose file to test against, or just try to inspect if any containers exist
    # If no containers, we can't reproduce easily without mocking.
    # But let's check attributes of a dummy container object if we can, 
    # or just trust that python_on_whales Container structure.
    
    # Let's try to list containers if any
    try:
        # Assuming current dir has compose
        client = DockerClient(compose_project_directory=os.getcwd())
        containers = client.compose.ps()
        if containers:
            c = containers[0]
            print(f"Container type: {type(c)}")
            print(f"Dir: {dir(c)}")
            # Try to access labels
            try:
                print(f"Labels: {c.labels}")
            except Exception as e:
                print(f"Error accessing labels: {e}")
                
            # helper to find where labels are
            if hasattr(c, 'config') and hasattr(c.config, 'labels'):
                 print(f"Found via config.labels: {c.config.labels}")
        else:
            print("No containers found to debug.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug()
