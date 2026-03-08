import typer
from python_on_whales import docker
from app.utils.ui import TableDisplay, TextDisplay

# --- Constants & Configuration ---
COLUMN_CONFIG = {
    "id": {"header": "ID", "style": "dim white", "no_wrap": True},
    "name": {"header": "NAME", "style": "blue", "no_wrap": True, "min_width": 10},
    "image": {"header": "IMAGE", "style": "cyan", "no_wrap": False, "ratio": 1},
    "status": {"header": "STATUS", "style": "white", "no_wrap": True},
    "ports": {"header": "PORTS", "style": "white", "no_wrap": False, "ratio": 1},
    "health": {"header": "HEALTH", "style": "white", "no_wrap": True},
    "network": {"header": "NETWORK", "style": "white", "no_wrap": False, "ratio": 1},
    "labels": {"header": "LABELS", "style": "white", "no_wrap": False, "ratio": 2},
    "mounts": {"header": "MOUNTS", "style": "white", "no_wrap": False, "ratio": 3},
    "fmounts": {"header": "FULL MOUNTS", "style": "white", "no_wrap": False, "ratio": 4},
    "volumes": {"header": "VOLUMES", "style": "white", "no_wrap": False, "ratio": 3},
    "command": {"header": "COMMAND", "style": "dim white", "no_wrap": False, "ratio": 1},
    "created": {"header": "CREATED", "style": "dim white", "no_wrap": True},
}

# --- Formatting Helpers ---
def shorten_image(image_name: str) -> str:
    """Shortens long image names by truncating the repository part."""
    if not image_name or ":" not in image_name:
        return image_name
    parts = image_name.split("/")
    if len(parts) > 1:
        return f".../{parts[-1]}"
    return image_name

def format_mounts(mounts, shorten: bool = True) -> str:
    """Formats mount paths for clean table display. shortening is optional."""
    paths = []
    for m in mounts:
        src, dest = m.source, m.destination
        
        # Shorten internal docker volume paths
        if shorten and src.startswith("/var/lib/docker/volumes/"):
            parts = src.split("/")
            if len(parts) > 5:
                src = f"vol:{parts[5][:8]}..."
        
        # Shorten long host paths
        elif shorten and len(src) > 30:
            sep = "/" if "/" in src else "\\"
            src_parts = src.split(sep)
            if len(src_parts) > 3:
                src = f"...{sep}{sep.join(src_parts[-2:])}"
        
        # Shorten long destination paths
        if shorten and len(dest) > 20:
            dest_parts = dest.split("/")
            if len(dest_parts) > 2:
                dest = f".../{dest_parts[-1]}"

        paths.append(f"{src}:{dest}")
    return "\n".join(paths) if paths else "-"

def get_container_data(container, key: str) -> str:
    """Extracts and formats specific data from a container object."""
    if key == "id":
        return container.id[:12]
    if key == "name":
        return container.name
    if key == "image":
        return shorten_image(container.config.image)
    if key == "status":
        return container.state.status.capitalize()
    if key == "ports":
        if not container.network_settings.ports:
            return "-"
        mappings = []
        for cp, hm in container.network_settings.ports.items():
            if hm:
                for m in hm:
                    mappings.append(f"{m.get('HostIp', '0.0.0.0')}:{m.get('HostPort')}->{cp}")
        return "\n".join(mappings) if mappings else "-"
    if key == "health":
        if not hasattr(container.state, 'health') or not container.state.health:
            return "-"
        h_status = container.state.health.status
        color = "green" if h_status == "healthy" else "yellow" if h_status == "starting" else "red"
        return f"[{color}]{h_status.capitalize()}[/]"
    if key == "network":
        return "\n".join(container.network_settings.networks.keys()) if container.network_settings.networks else "-"
    if key == "labels":
        return "\n".join([f"{k}={v}" for k, v in container.config.labels.items()]) if container.config.labels else "-"
    if key == "mounts":
        return format_mounts(container.mounts)
    if key == "fmounts":
        return format_mounts(container.mounts, shorten=False)
    if key == "volumes":
        return format_mounts([m for m in container.mounts if m.type == "volume"])
    if key == "command":
        return container.config.cmd[0] if container.config.cmd else "-"
    if key == "created":
        return container.created.strftime("%Y-%m-%d %H:%M:%S") if hasattr(container, 'created') else "-"
    return "-"

def get_status_indicator(container) -> str:
    """Returns a colored status dot for the container."""
    dot = "●"
    if container.state.paused:
        return f"[yellow]{dot}[/yellow]"
    if container.state.running:
        return f"[green]{dot}[/green]"
    return f"[red]{dot}[/red]"

def parse_format_flag(format_str: str) -> list:
    """Parses the --format flag into a list of column keys."""
    fmt = format_str.strip()
    if fmt.startswith("{{") and fmt.endswith("}}"):
        fmt = fmt[2:-2].strip()
    return [k.strip().lower() for k in fmt.split(",") if k.strip()]

# --- Main Command ---
def _status(
    all_containers: bool = False,
    stopped: bool = False,
    paused: bool = False,
    show_volume: bool = False,
    show_id: bool = False,
    show_health: bool = False,
    show_network: bool = False,
    show_labels: bool = False,
    show_mounts: bool = False,
    format: str = None,
):
    """
    Shows a clean, beautiful table of container statuses with flexible formatting.
    (Core logic separated from Typer for better modularity and testability).
    """
    try:
        # 1. Fetch Containers
        filters = {}
        if stopped: filters["status"] = "exited"
        elif paused: filters["status"] = "paused"
        
        containers = docker.container.list(all=all_containers or stopped or paused, filters=filters)
        if not containers:
            TextDisplay.info_text("No containers found.")
            return

        # 2. Determine Active Columns
        active_keys = []
        if format:
            requested_keys = parse_format_flag(format)
            for k in requested_keys:
                if k in COLUMN_CONFIG:
                    active_keys.append(k)
                else:
                    TextDisplay.warn_text(f"Unknown column: {k}")
        else:
            active_keys = ["name", "image", "status", "ports"]
            if show_id: active_keys.insert(0, "id")
            if show_health: active_keys.append("health")
            if show_network: active_keys.append("network")
            if show_labels: active_keys.append("labels")
            if show_mounts: active_keys.append("mounts")
            if show_volume: active_keys.append("volumes")

        # 3. Build & Show Table
        columns = [{"header": "", "style": "white", "no_wrap": True}] # Indicator
        columns.extend([COLUMN_CONFIG[k] for k in active_keys])
        
        table = TableDisplay(title="[bold blue]Mate Status[/bold blue]", columns=columns)

        for container in containers:
            row = [get_status_indicator(container)]
            row.extend([get_container_data(container, k) for k in active_keys])
            
            style = "green" if container.state.running else "yellow" if container.state.paused else "red"
            table.add_row(row, style=style)

        table.show()

    except Exception as e:
        TextDisplay.error_text(f"Error fetching container status: {str(e)}")

def status(
    all_containers: bool = typer.Option(False, "--all", "-a", help="Show all containers (default shows just running)"),
    stopped: bool = typer.Option(False, "--stopped", help="Show only stopped containers"),
    paused: bool = typer.Option(False, "--paused", help="Show only paused containers"),
    show_volume: bool = typer.Option(False, "--volume", "-v", help="Show mounted volumes"),
    show_id: bool = typer.Option(False, "--id", help="Show container ID"),
    show_health: bool = typer.Option(False, "--health", help="Show container health"),
    show_network: bool = typer.Option(False, "--network", help="Show container network"),
    show_labels: bool = typer.Option(False, "--labels", help="Show container labels"),
    show_mounts: bool = typer.Option(False, "--mounts", help="Show container mounts"),
    format: str = typer.Option(None, "--format", help="Custom format for status output (e.g., 'name,image,mounts' or '{{ name, image }}')"),
):
    """
    Shows a clean, beautiful table of container statuses with flexible formatting.
    """
    _status(
        all_containers=all_containers,
        stopped=stopped,
        paused=paused,
        show_volume=show_volume,
        show_id=show_id,
        show_health=show_health,
        show_network=show_network,
        show_labels=show_labels,
        show_mounts=show_mounts,
        format=format
    )
