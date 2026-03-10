# mate up

The `up` command is the heart of DevMate. It builds, starts, and validates your entire development stack with zero configuration required from the user.

## Detailed Description
When you call `up`, DevMate performs "Intelligent Orchestration":
- **Detection**: Scans for `compose.yaml` or `Dockerfile`.
- **Building**: Automatically builds images if they don't exist (or if `--force` is used).
- **Execution**: Starts the containers in detached mode.
- **Verification**: Runs health checks. For Compose, it even checks internal service-to-service connectivity.

## Usage
`mate up [OPTIONS]`

## Options
| Flag | Description |
|------|-------------|
| `--path` | Directory to look for configuration files. |
| `-p`, `--port` | Port mappings (`HOST:CONTAINER`) for Dockerfile projects. |
| `--pull` | Image pull policy: `always`, `missing`, or `never`. |
| `-f`, `--force` | Force a fresh build and restart. |

## Examples

### 1. Multi-Service (Compose)
Starts a database, API, and frontend simultaneously and checks their health.
```bash
mate up
```

### 2. Single Service (Dockerfile)
Builds the current directory and maps it to port 3000.
```bash
mate up --port 3000:3000
```

### 3. Fresh Start (Forced Rebuild)
Useful when you've changed your Dockerfile or dependencies and need a clean slate.
```bash
mate up --force --pull always
```
