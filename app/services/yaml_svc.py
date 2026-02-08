from pathlib import Path
import yaml

def load_compose(path: str) -> dict:
    with open(Path(path).resolve(), "r") as f:
        return yaml.safe_load(f)

def extract_ports_from_compose(compose: dict) -> dict[str, list[str]]:
    
    services = compose.get("services", {})
    ports_map: dict[str, list[str]] = {}

    for service_name, service in services.items():
        ports = service.get("ports", [])
        extracted_ports = []

        for port in ports:
            if isinstance(port, str):
                extracted_ports.append(port)

            elif isinstance(port, dict):
                published = port.get("published")
                target = port.get("target")
                if published and target:
                    extracted_ports.append(f"{published}:{target}")

        if extracted_ports:
            ports_map[service_name] = extracted_ports

    return ports_map

def flatten_ports(port_map: dict[str, list[str]]) -> list[str]:
    return [p for ports in port_map.values() for p in ports]

def classify_services(compose: dict):
    services = compose.get("services", {})

    exposed = {}
    internal = {}

    for name, svc in services.items():
        ports = svc.get("ports", [])
        if ports:
            exposed[name] = ports
        else:
            internal[name] = svc

    return exposed, internal


def get_service_internal_port(service_config: dict) -> int | None:
    """
    Attempts to find a port to check for an internal service.
    Prioritizes:
    1. 'ports' target (even if not published, sometimes defined here)
    2. 'expose' list
    3. Default to 80 if nothing else found? Or None.
    """
    
    # Check ports section for target
    ports = service_config.get("ports", [])
    for port in ports:
        if isinstance(port, dict):
            target = port.get("target")
            if target:
                return int(target)
        elif isinstance(port, str):
            # "80:80" or "80"
            parts = port.split(":")
            if len(parts) > 1:
                return int(parts[1])
            else:
                return int(parts[0])

    # Check expose section
    expose = service_config.get("expose", [])
    if expose:
        return int(expose[0])
        
    return None


def has_native_healthcheck(service_config: dict) -> bool:
    """
    Checks if the service definition has a 'healthcheck' block.
    """
    return "healthcheck" in service_config


