# mate down

The `down` command stops and cleans up your development environment. It is designed to safely terminate processes and optionally remove transient assets like volumes and images.

## Detailed Description
`mate down` automatically detects your environment type. For Compose projects, it stops and removes containers and networks. For standalone containers, it terminates the specific process. Use this when you want to free up system resources or reset your environment.

## Usage
`mate down [OPTIONS]`

## Options
| Flag | Description |
|------|-------------|
| `-p`, `--project-path` | Path to the project. DevMate detects the config here. |
| `-c`, `--container-name` | Explicitly stop a container by name, ignoring project logic. |
| `-v`, `--remove-volumes` | Remove named and anonymous volumes (use with caution). |
| `-i`, `--remove-images` | Remove images used by the services. |
| `-o`, `--remove-orphans` | Clean up containers not defined in the current compose file. |

## Examples

### 1. Docker Compose Cleanup
Stops all services defined in the current directory's Compose file.
```bash
mate down
```

### 2. Dockerfile Cleanup (Full Reset)
Stops the container and removes its images and volumes.
```bash
mate down -v -i
```

### 3. Direct Container Stop
Stops a specific container named "legacy-db" without needing a manifest file.
```bash
mate down --container-name legacy-db
```
