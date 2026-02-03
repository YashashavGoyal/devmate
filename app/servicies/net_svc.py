import time
import requests
from requests.exceptions import RequestException, ConnectionError, Timeout

from app.utils import ProgressBar

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