import time
import traceback
from typer import Option, Exit
from typing import List
from pathlib import Path


from app.utils import TextDisplay, TableDisplay
from app.services import (
    detect_configuration, 
    start_compose, 
    build_dockerfile, 
    run_container,
    check_health, # http check
    check_host_port, # tcp check
    check_internal_tcp, # internal docker check
    load_compose, 
    classify_services, 
    get_service_internal_port,
    has_native_healthcheck,
    get_project_containers,
    get_container_health,
    has_nc,
    get_image_exposed_ports,
    ConfigType
)

def up(
    path: str = Option(".", "--path", help="Path where the config file is present"),
    port: List[str] = Option([], "-p", "--port", help="Port mappings in HOST:CONTAINER format (e.g. -p 8080:80)"),
    pull: str = Option("missing", help="Pull policy: always, missing, never. for compose"),
    force: bool = Option(False, "-f", "--force", help="Force restart container")
):
    
    try:
        config_mode = detect_configuration(path=path)
    except Exception as e:
        TextDisplay.error_text(f"Error: {e}")
        Exit(1)

    if config_mode == ConfigType.NONE:
        TextDisplay.error_text("Config files didn't present in current directory")
        Exit(1)
    
    try:
        if config_mode == ConfigType.COMPOSE:
            start_compose(path=path, pull=pull)
            

            TextDisplay.info_text("Performing Health Checks...")
            
            compose_path = None

            p = Path(path).resolve()
            possible_files = ["compose.yaml", "compose.yml", "docker-compose.yaml", "docker-compose.yml"]
            for f in possible_files:
                if (p / f).exists():
                    compose_path = p / f
                    break
            
            if not compose_path:
                TextDisplay.error_text("Compose file found during detection but lost now?")
                return

            compose_data = load_compose(str(compose_path))
            exposed_services, internal_services = classify_services(compose_data)
            
            results = []

            # Check Services
            
            # Map of service name to container (if found)
            containers = get_project_containers(path)
            service_container_map = {}
            if containers:
                for c in containers:
                    # Check for labels in potential locations
                    labels = {}
                    if hasattr(c, 'labels'):
                         labels = c.labels
                    elif hasattr(c, 'config') and hasattr(c.config, 'labels'):
                         labels = c.config.labels
                    
                    svc_name = labels.get("com.docker.compose.service")
                    if svc_name:
                        service_container_map[svc_name] = c

            
            # Helper to check if we can run internal checks
            source_container = None
            if containers:
                candidate_fallback = None
                candidate_exposed = None

                for c in containers:
                    if not has_nc(c.name):
                        continue
                    
                    # Check for labels in potential locations
                    labels = {}
                    if hasattr(c, 'labels'):
                         labels = c.labels
                    elif hasattr(c, 'config') and hasattr(c.config, 'labels'):
                         labels = c.config.labels
                    
                    service_name = labels.get("com.docker.compose.service")
                    if service_name and service_name in exposed_services:
                        candidate_exposed = c
                        break 
                    
                    if candidate_fallback is None:
                        candidate_fallback = c
                
                source_container = candidate_exposed or candidate_fallback


            all_services = set(exposed_services.keys()) | set(internal_services.keys())
            
            for name in all_services:
                # Get service definition
                svc_def = exposed_services.get(name) or internal_services.get(name)
                
                status = "UNKNOWN"
                details = "Service not found in analysis?"
                
                # 1. PRIORITY: Native Health Check
                if has_native_healthcheck(svc_def):
                    container = service_container_map.get(name)
                    if container:
                        health = get_container_health(container.name)
                        if health == "healthy":
                            status = "UP"
                            details = "Native Docker Health Check Passed"
                        else:
                            status = "DOWN"
                            details = f"Native Check: {health}"
                    else:
                        status = "DOWN"
                        details = "Container not found for native check"
                
                # 2. Fallback: Exposed Check
                elif name in exposed_services:
                    port_def = exposed_services[name]
                    host_port = None
                    for pd in port_def:
                        if isinstance(pd, str):
                            host_port = int(pd.split(":")[0])
                        elif isinstance(pd, dict) and "published" in pd:
                            host_port = int(pd["published"])
                        if host_port: break
                    
                    if host_port:
                        is_up = check_host_port(host_port)
                        status = "UP" if is_up else "DOWN"
                        details = f"localhost:{host_port} ({'Port Open' if is_up else 'Port Closed'})"
                    else:
                        details = "No host port found"

                # 3. Fallback: Internal Check
                elif name in internal_services:
                    if source_container:
                        target_port = get_service_internal_port(svc_def)
                        if target_port:
                            # Use container name as hostname
                            target_host = name
                            if name in service_container_map:
                                target_host = service_container_map[name].name
                            TextDisplay.info_text(f"Checking {target_host}:{target_port} from {source_container.name}")
                            is_up = check_internal_tcp(source_container.name, target_host, target_port)
                            status = "UP" if is_up else "DOWN"
                            details = f"{target_host}:{target_port} from {source_container.name}"
                        else:
                            details = "No internal port defined"
                    else:
                        status = "SKIPPED"
                        details = "No source container for internal check"

                results.append({"name": name, "type": "Native" if has_native_healthcheck(svc_def) else ("Exposed" if name in exposed_services else "Internal"), "status": status, "details": details})



            # Display Report
            table = TableDisplay(
                title="Service Health Report",
                columns=["Service", "Type", "Status", "Details"]
            )

            for res in results:
                status_style = "green" if res["status"] == "UP" else "red"
                table.add_row([
                    res["name"], 
                    res["type"], 
                    f"[{status_style}]{res['status']}[/{status_style}]", 
                    res["details"]
                ])

            table.show()


        if config_mode == ConfigType.DOCKERFILE:
            # Check exposed ports
            dockerfile_path = Path(path).resolve() / "Dockerfile"
            exposed_ports = get_image_exposed_ports(str(dockerfile_path))
            
            # User ports are in format HOST:CONTAINER
            # We need to check if CONTAINER port is in exposed_ports
            if exposed_ports:
                if not port:
                    # Case 1: auto-map exposed ports
                    port = [f"{p}:{p}" for p in exposed_ports]
                    TextDisplay.info_text(f"No ports provided. Auto-mapping exposed ports: {port}")
                else: 
                    # Case 2: validate user provided ports and merge missing exposed ports
                    user_mapped_container_ports = set()
                    for p in port:
                        parts = p.split(":")
                        if len(parts) >= 2:
                            container_port = parts[-1]
                            user_mapped_container_ports.add(container_port)
                            if container_port not in exposed_ports:
                                TextDisplay.warn_text(f"Warning: Port {container_port} is mapped but not exposed in Dockerfile (Exposed: {', '.join(exposed_ports)})")
                    
                    # Add missing exposed ports
                    added_ports = []
                    for ep in exposed_ports:
                        if ep not in user_mapped_container_ports:
                            mapping = f"{ep}:{ep}"
                            port.append(mapping)
                            added_ports.append(mapping)
                    
                    if added_ports:
                        TextDisplay.info_text(f"Added missing exposed ports: {added_ports}")

            img = build_dockerfile(path=path)
            TextDisplay.info_text(f"{img} is completely build ....")

            container = run_container(
                image_name=img,
                ports=port,
                start_new=force,
                detach=True
            )
            
            time.sleep(2)
            
            TextDisplay.info_text(f"Starting {container} ....")

            TextDisplay.info_text("Perfoming health check ....")
            host_port = [int(p.split(":",1)[0]) for p in port]
            
            table = TableDisplay(
                title="Container Health Report",
                columns=["Port", "Status", "Message"]
            )

            for p in host_port:
                # Try HTTP first for Dockerfile single service
                res = check_health(f"http://localhost:{p}", max_retries=5)
                if res["success"]:
                     table.add_row([f"{p}", "[green]UP[/green]", res["message"]])
                else:
                    # Fallback to TCP
                    is_up = check_host_port(p)
                    if is_up:
                         table.add_row([f"{p}", "[green]UP (TCP)[/green]", "Port is open, but HTTP failed"])
                    else:
                         table.add_row([f"{p}", "[red]DOWN[/red]", "Port unreachable"])
            
            table.show()

    except Exception as e:
        # traceback.print_exc()
        TextDisplay.error_text(f"An error occurred: {e}")
