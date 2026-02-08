import time
import requests
import socket
from python_on_whales import docker
from requests.exceptions import RequestException, ConnectionError, Timeout

from app.utils import ProgressBar, TextDisplay

def check_health(
    url: str, 
    max_retries: int = 3, 
    timeout: int = 5, 
    delay: int = 1,
    progress: ProgressBar = None
):
    """
    Pings a URL to see if it returns a 200 OK.
    Retries automatically to allow containers time to spin up.
    
    Returns:
        dict: {"success": bool, "status_code": int, "message": str}
    """
    for attempt in range(1, max_retries + 1):

        if progress:
            progress.set_description(
                f"Checking health ({attempt}/{max_retries})"
            )

        start = time.time()

        try:
            response = requests.get(url, timeout=timeout)
            end = time.time()
            elapsed = end - start

            if 200 <= response.status_code < 300:
                if progress:
                    progress.finish()
                    
                return {
                    "success": True, 
                    "status_code": response.status_code, 
                    "message": f"Service is healthy (responded in {elapsed:.2f}s)"
                }

            else:
                error = {
                    "success": False, 
                    "status_code": response.status_code, 
                    "message": "Service returned non-2xx status"
                }

        except (RequestException, ConnectionError, Timeout) as e:
            error = {
                "success": False, 
                "status_code": None, 
                "message": f"Service is not reachable: {str(e)}"
            }

        if progress:
            progress.advance()

        if attempt < max_retries + 1:
            time.sleep(delay)

    return error

def check_host_port(port: int, host: str = "127.0.0.1", timeout=2) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def check_internal_tcp(
    source_container: str,
    target_service: str,
    port: int,
) -> bool:
    try:
        docker.container.execute(
            source_container,
            ["nc", "-z", target_service, str(port)],
        )
        return True
    except Exception:
        return False


def has_nc(container: str) -> bool:
    """
    Checks if 'nc' (netcat) is available in the container.
    """
    cmd_variants = [
        ["which", "nc"],
        ["sh", "-c", "command -v nc"],
        ["sh", "-c", "whereis nc"] # fallback
    ]
    
    errors = []
    for cmd in cmd_variants:
        try:
            docker.container.execute(container, cmd)
            return True
        except Exception as e:
            errors.append(f"{cmd}: {e}")
            continue
            
    TextDisplay.debug_text(f"Health Check Debug: 'nc' check failed for {container}. Errors: {errors}")
    return False