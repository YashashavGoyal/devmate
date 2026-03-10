# mate deploy

The `deploy` command is the fastest way to get a project running. it combines `clone` and `up` into a single atomic operation, including automatic environment detection and health checks.

## Detailed Description
When you run `deploy`, DevMate:
1. Clones the repository to your local machine.
2. Enters the project directory (or a specified sub-location).
3. Detects if the project uses Docker Compose or a standalone Dockerfile.
4. Spins up the services.
5. Performs immediate health checks to ensure the application is ready.

## Usage
`mate deploy <REPO_URL> [OPTIONS]`

## Arguments & Options
| Flag | Description |
|------|-------------|
| `REPO_URL` | The Git URL to clone (required). |
| `-n`, `--name` | Custom name for the cloned folder. |
| `-b`, `--branch` | Specific branch to clone (e.g., `main`, `staging`). |
| `-p`, `--port` | Port mappings for Dockerfile projects (`HOST:CONTAINER`). |
| `-l`, `--location` | Subdirectory inside the repo where config files are found (default `.`). |
| `-f`, `--force` | Force rebuild of images and restart. |

## Examples

### 1. Docker Compose Scenario (Default)
Deploys a multi-container stack from a standard repository.
```bash
mate deploy https://github.com/example/api-stack.git
```

### 2. Dockerfile Scenario (with Port Mapping)
Deploys a single service and maps it to a specific local port.
```bash
mate deploy https://github.com/example/web-app.git --port 8080:80
```

### 3. Custom Branch and Sub-location
Deploys the `dev` branch and looks for configuration in the `./backend` folder.
```bash
mate deploy https://github.com/example/monorepo.git --branch dev --location ./backend
```
