import typer
from python_on_whales import docker
from app.utils.ui import TableDisplay, TextDisplay

def status(
    all_containers: bool = typer.Option(False, "--all", "-a", help="Show all containers (default shows just running)"),
    stopped: bool = typer.Option(False, "--stopped", help="Show only stopped containers"),
    paused: bool = typer.Option(False, "--paused", help="Show only paused containers"),
    show_volume: bool = typer.Option(False, "--volume", "-v", help="Show mounted volumes"),
    show_id: bool = typer.Option(False, "--id", help="Show container ID"),
):
    """
    Clean, beautiful table showing relevant info for your API/Services.
    """
    try:
        # Fetch containers based on flags
        if stopped:
            containers = docker.container.list(filters={"status": "exited"})
        elif paused:
            containers = docker.container.list(filters={"status": "paused"})
        elif all_containers:
            containers = docker.container.list(all=True)
        else:
            containers = docker.container.list()

        if not containers:
            TextDisplay.info_text("No containers found.")
            return

        # Prepare columns
        columns = ["", "NAME", "IMAGE", "STATUS", "PORTS"]
        if show_id:
            columns.insert(1, "ID")
        if show_volume:
            columns.append("VOLUMES")

        table = TableDisplay(title="[bold blue]Mate Status[/bold blue]", columns=columns)

        for container in containers:
            # python-on-whales container object has state.status and state.running etc.
            # We can use container.state.status and container.state.started_at
            
            status_text = container.state.status.capitalize()
            
            # Indicator Dot
            indicator = "●"
            if container.state.paused:
                indicator = f"[yellow]{indicator}[/yellow]"
            elif container.state.running:
                indicator = f"[green]{indicator}[/green]"
            else:
                indicator = f"[red]{indicator}[/red]"

            # Parse Ports
            # Ports (0.0.0.0:8000->80/tcp)
            port_mappings = []
            if container.network_settings.ports:
                for container_port, host_mappings in container.network_settings.ports.items():
                    if host_mappings:
                        for mapping in host_mappings:
                            host_ip = mapping.get("HostIp", "0.0.0.0")
                            host_port = mapping.get("HostPort")
                            port_mappings.append(f"{host_ip}:{host_port}->{container_port}")
                    else:
                        port_mappings.append(container_port)
            
            ports_str = ", ".join(port_mappings) if port_mappings else "-"

            # Row Data
            row = [indicator, container.name, container.config.image, status_text, ports_str]
            
            if show_id:
                row.insert(1, container.id[:12])
            
            if show_volume:
                mounts = [f"{m.source}:{m.destination}" for m in container.mounts]
                row.append(", ".join(mounts) if mounts else "-")

            # Style based on status
            if container.state.paused:
                style = "yellow"
            elif container.state.running:
                style = "green"
            else:
                style = "red"
            
            table.add_row(row, style=style)

        table.show()

    except Exception as e:
        TextDisplay.error_text(f"Error fetching container status: {str(e)}")
