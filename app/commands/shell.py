from typer import Option, Exit
from python_on_whales import DockerException

from app.services import detect_configuration, ConfigType, get_project_containers, container_shell 
from app.utils import TextDisplay, Prompt

def shell(
    name: str | None = Option(None, "-n", "--name", help="Name of the container or service (Compose)"),
    shell_path: str = Option("/bin/sh", "-s", "--shell", "--sh", help="Shell to use for connecting container"),
    path: str = Option(".", "-p", "--path", help="Path to the project directory"),
):

    try:
        config_mode = detect_configuration(path)
    
        if config_mode == ConfigType.NONE:
            if not name:
                TextDisplay.error_text("Container name required when no config is detected.")
                raise Exit(1)
            try:
                container_shell(name, shell_path)
            except DockerException as de:
                TextDisplay.error_text(f"Error: {de}")
                raise Exit(1)
            return
        
        if config_mode == ConfigType.COMPOSE:
            containers = get_project_containers(path, return_names=True) 
            if not containers:
                TextDisplay.error_text("No containers found.")
                raise Exit(1)
            if name:
                if name not in containers:
                    TextDisplay.error_text(f"Container '{name}' not found.")
                    raise Exit(1)
                try:
                    container_shell(name, shell_path)
                except DockerException as de:
                    TextDisplay.error_text(f"Error: {de}")
            else:
                if len(containers) > 1:
                    TextDisplay.warn_text("Multiple containers found.")
                    TextDisplay.info_text("Pick the container name (or use -n / --name option).")
                    selected_container = Prompt.select("Container Name: ", containers)
                    try:
                        container_shell(selected_container, shell_path)
                    except DockerException as de:
                        TextDisplay.error_text(f"Error: {de}")
                else:
                    try:
                        container_shell(containers[0], shell_path)
                    except DockerException as de:
                        TextDisplay.error_text(f"Error: {de}")
            return

        elif config_mode == ConfigType.DOCKERFILE:
            if not name:
                TextDisplay.error_text("Container name required when dockerfile is detected.")
                raise Exit(1)
            try:
                container_shell(name, shell_path)
            except DockerException as de:
                TextDisplay.error_text(f"Error: {de}")
            return

    except Exception as e:
        TextDisplay.error_text(f"Error: {e}")
        raise Exit(1)