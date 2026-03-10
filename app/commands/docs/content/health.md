# mate health

The `health` command verifies that your application is not just running, but actually responding to requests.

## Detailed Description
`mate health` performs active polling against your application's endpoints. It supports both HTTP (for web apps) and TCP (for databases/internal services). It includes built-in retry logic and progress tracking to handle applications with slow startup times.

## Usage
`mate health [OPTIONS]`

## Options
| Flag | Description |
|------|-------------|
| `-u`, `--url` | Base URL (e.g., `http://localhost`). |
| `-p`, `--path` | Endpoint path (default: `/`). |
| `-P`, `--port` | Port to check. |
| `-r`, `--max-retries` | How many times to try before giving up (default: 3). |
| `-t`, `--timeout` | Seconds to wait for each request. |

## Examples

### 1. Web Service Check
Checks if your frontend is serving traffic on the root path.
```bash
mate health --port 3000
```

### 2. API Health Endpoint
Verifies a specific internal status endpoint with multiple retries.
```bash
mate health -P 8080 -p /api/v1/health --max-retries 10
```

### 3. Remote Service Audit
Checks the health of an external or staging URL.
```bash
mate health --url http://staging.myapp.com --timeout 10
```
