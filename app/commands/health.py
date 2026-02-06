from typer import Option

from app.services import check_health
from app.utils import TextDisplay, ProgressBar

def health(
    url: str = Option("http://localhost", "--url", "-u", help="URL to check."),
    path: str = Option("/", "--path", "-p", help="Path to check."),
    port: int = Option(None, "--port", "-P", help="Port to check."),
    max_retries: int = Option(3, "--max-retries", "-r", help="Maximum number of retries."),
    timeout: int = Option(5, "--timeout", "-t", help="Timeout in seconds."),
    delay: int = Option(1, "--delay", "-d", help="Delay between retries."),
):
    """
    Checks if the application is running and responding.
    You can use this command to check if the application is running and responding.
    Design for local development but can be used for remote applications.
    """
    
    if port:
        url = f"{url}:{port}"

    if "http" not in url:
        url = f"http://{url}"

    route = f"{url}{path}"

    TextDisplay.style_text(f"Checking health of {route}  ...\n", "cyan")
    with ProgressBar(max_retries, "Checking health") as progress:
        result = check_health(route, max_retries, timeout, delay, progress)
    
    if result["success"]:
        TextDisplay.style_text("Service is healthy", "green")
        TextDisplay.print_json(json=result)

    else:
        TextDisplay.error_text(f"Service is not reachable")
        TextDisplay.print_json(json=result)



