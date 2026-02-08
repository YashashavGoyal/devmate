from python_on_whales import docker, DockerClient
from pathlib import Path
from enum import Enum

class ConfigType(Enum):
    COMPOSE = "compose"
    DOCKERFILE = "dockerfile"
    NONE = "none"

class PullPolicy(Enum):
    MISSING = "missing"
    NEVER = "never"
    ALWAYS = "always"


def detect_configuration(path: str) -> ConfigType:

    path = Path(path).absolute().expanduser().resolve()

    if not path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")


    compose_files = {
        "compose.yaml",
        "compose.yml",
        "docker-compose.yaml",
        "docker-compose.yml",
    }

    if any((path / f).exists() for f in compose_files):
        return ConfigType.COMPOSE

    if (path / "Dockerfile").exists():
        return ConfigType.DOCKERFILE
    
    return ConfigType.NONE


def start_compose(
    path: str, 
    compose_file: str | None = None, 
    pull: str | None = None
):

    compose_dir = Path(path).absolute().expanduser().resolve()

    compose_candidates = [
        compose_file,
        "docker-compose.yaml",
        "docker-compose.yml",
        "compose.yaml",
        "compose.yml",
    ]

    compose_path = None
    for file in compose_candidates:
        if file and (compose_dir / str(file)).exists():
            compose_path = compose_dir / str(file)
            break

    if not compose_path:
        raise FileNotFoundError("Docker Compose file not found")

    if pull and pull not in {p.value for p in PullPolicy}:
            raise ValueError("Not Value For Pull Always, values must be ['missing', 'never', 'always']")

    client = DockerClient(
        compose_files=[str(compose_path)],
        compose_project_directory=str(compose_dir)
    )

    client.compose.up(
        detach=True, 
        build=True,
        pull=pull
    )


def build_dockerfile(
    path: str,
    image_name: str | None = None,
    build_args: dict[str, str] | None = None,
) -> str:

    build_dir = Path(path).expanduser().absolute().resolve()
    if (build_dir / "Dockerfile").exists():
        build_file = build_dir / "Dockerfile"

    else:
        raise FileNotFoundError("Dockerfile Not Found")
    

    if not image_name:
        image_name = f"{build_dir.name}:latest"
    
    docker.build(
        context_path=str(build_dir),
        file=str(build_file),
        build_args=build_args or {},
        tags=[image_name],
    )

    return image_name

def get_image_exposed_ports(dockerfile_path: str) -> list[str]:
    """
    Returns a list of exposed ports from a Dockerfile.
    """
    if not Path(dockerfile_path).exists():
        raise FileNotFoundError("Dockerfile path not found")
    
    ports = []
    with open(dockerfile_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.upper().startswith("EXPOSE"):
                # Handle "EXPOSE 80 443" or "EXPOSE 80/tcp"
                parts = line[6:].strip().split()
                for p in parts:
                    # Remove protocol if present (e.g. 80/tcp -> 80)
                    port = p.split("/")[0]
                    ports.append(port)
    return ports
    

def normalize_ports(port_list: list[str]) -> list[tuple]:
    published = []
    for p in port_list or []:
        host, container = p.split(":", 1)
        published.append((container, host))
    return published

def run_container(
    image_name: str,
    container_name: str | None = None,
    ports: list[str] | None = None,
    start_new: bool = False,
    volumes: list[str] | None = None,
    detach: bool = False,
) -> str:

    if not image_name:
        raise ValueError("Image Not Found, check for image name and version/tag")
    
    if not container_name:
        container_name = f"{image_name.split(':')[0]}_app"

    if docker.container.exists(container_name):
        if start_new:
            docker.container.stop(container_name)
            docker.container.remove(container_name, force=True)

        else:
            raise RuntimeError("Container Already Exist")

    ports = normalize_ports(port_list=ports)

    docker.container.run(
        image=image_name, 
        name=container_name,
        volumes=volumes or [],
        publish=ports or [],
        detach=detach
    )

    return container_name


def get_project_containers(path: str) -> list[str]:
    """
    Returns a list of container objects/names for the given compose project path.
    """
    project_dir = Path(path).absolute().expanduser().resolve()
    
    client = DockerClient(compose_project_directory=str(project_dir))
    return client.compose.ps()


def get_container_health(container_name: str) -> str | None:
    """
    Returns the health status of a container (e.g. 'healthy', 'unhealthy', 'starting').
    Returns None if no health check is defined or container not found.
    """
    try:
        inspect_data = docker.container.inspect(container_name)
        # docker.container.inspect returns a Container object.
        # Container.state is a helper object usually.
        # Assuming inspect returns object with .state.health.status.
        
        if inspect_data.state.health:
            return inspect_data.state.health.status
        return None
    except Exception:
        return None


