from typer import Option
from app.utils import TextDisplay
from app.services import detect_configuration, compose_down, container_down, ConfigType


def down(
    project_path: str = Option(".", "-p", "--project-path", help="Path to the project directory"),
    container_name: str = Option("", "-c", "--container-name", help="Name of the container (project path ignored)"),
    remove_volumes: bool = Option(False, "-v", "--remove-volumes", help="Remove volumes"),
    remove_images: bool = Option(False, "-i", "--remove-images", help="Remove images"),
    remove_orphans: bool = Option(False, "-o", "--remove-orphans", help="Remove orphan containers"),
):
    try:
        if container_name:
            container_down(container_name, remove_volumes, remove_images)
            return

        config_type = detect_configuration(project_path)
        if config_type == ConfigType.COMPOSE:
            compose_down(project_path, remove_volumes, remove_images, remove_orphans)
        elif config_type == ConfigType.DOCKERFILE or config_type == ConfigType.NONE:
            container_down(container_name, remove_volumes, remove_images)
        else:
            raise Exception("Project configuration not detected or Container not found")

    except Exception as e:
        TextDisplay.error_text(f"Error: {e}")