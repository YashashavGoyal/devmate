from typer import Option

from app.utils import TextDisplay
from app.services import compose_logs, container_logs

def logs(
    path: str = Option(".", "-p", "--path", help="Path to the project directory"),
    tail: int = Option(100, "-t", "--tail", help="Number of lines to show"),
    follow: bool = Option(False, "-f", "--follow", help="Follow the logs"),
    container: str = Option(None, "-c", "--container", help="Container name"),
):
    
    if container:
        try:
            return container_logs(container, tail, follow)
        except Exception as e:
            TextDisplay.error_text(f"Error: {e}")
    else:
        try:
            return compose_logs(path, tail, follow)
        except Exception as e:
            TextDisplay.error_text(f"Error: {e}")